// Animation choreography via Motion (vendored UMD bundle exposing window.Motion).
// Everything is gated behind prefers-reduced-motion; CSS keyframe effects
// (floating paws, gallery marquee) are gated in styles.css the same way.
document.addEventListener("DOMContentLoaded", () => {
  if (typeof Motion === "undefined") return;
  const { animate, inView, scroll, stagger } = Motion;

  const showAll = () =>
    document
      .querySelectorAll(".fade-up, .hero-intro")
      .forEach((el) => (el.style.opacity = 1));

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    showAll();
    return;
  }

  const EASE_OUT = [0.22, 1, 0.36, 1];
  const SPRING = { type: "spring", stiffness: 300, damping: 20 };

  // --- Hero entrance: headline lines, tagline, buttons, then the shiba pops in ---
  const heroIntro = document.querySelectorAll(".hero-intro");
  if (heroIntro.length) {
    animate(
      heroIntro,
      { opacity: [0, 1], y: [30, 0] },
      { duration: 0.7, ease: EASE_OUT, delay: stagger(0.12) }
    );
  }
  const heroDog = document.getElementById("hero-dog");
  if (heroDog) {
    animate(
      heroDog,
      { opacity: [0, 1], scale: [0.85, 1], rotate: [-4, 0] },
      { ...SPRING, delay: 0.3 }
    );
  }

  // --- Scroll reveals: staggered groups first, then standalone fade-ups ---
  document.querySelectorAll("[data-stagger]").forEach((group) => {
    const items = group.querySelectorAll(".fade-up");
    if (!items.length) return;
    inView(
      group,
      () => {
        animate(
          items,
          { opacity: [0, 1], y: [32, 0] },
          { duration: 0.55, ease: EASE_OUT, delay: stagger(0.12) }
        );
      },
      { amount: 0.15 }
    );
  });

  document
    .querySelectorAll(".fade-up:not([data-stagger] .fade-up)")
    .forEach((el) => {
      inView(
        el,
        () => {
          animate(
            el,
            { opacity: [0, 1], y: [24, 0] },
            { duration: 0.6, ease: EASE_OUT }
          );
        },
        { amount: 0.2 }
      );
    });

  // --- Spring pop-ins (feature circles, CTA dogs) ---
  document.querySelectorAll("[data-pop]").forEach((el) => {
    inView(
      el,
      () => {
        animate(el, { scale: [0.6, 1], opacity: [0, 1] }, { ...SPRING });
      },
      { amount: 0.4 }
    );
  });

  // --- Scroll-linked parallax: data-parallax="<px drift>" ---
  document.querySelectorAll("[data-parallax]").forEach((el) => {
    const drift = parseFloat(el.dataset.parallax || "0");
    if (!drift) return;
    scroll(animate(el, { y: [-drift, drift] }, { ease: "linear" }), {
      target: el,
      offset: ["start end", "end start"],
    });
  });

  // --- Back-to-top paw ---
  const toTop = document.getElementById("back-to-top");
  if (toTop) {
    const toggle = () => {
      const show = window.scrollY > 600;
      toTop.classList.toggle("hidden", !show);
      toTop.classList.toggle("flex", show);
    };
    window.addEventListener("scroll", toggle, { passive: true });
    toggle();
    toTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});
