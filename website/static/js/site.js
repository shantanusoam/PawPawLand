// Animation choreography via Motion (vendored UMD bundle exposing window.Motion).
// Everything is gated behind prefers-reduced-motion; CSS keyframe effects
// (floating paws, gallery marquee) are gated in styles.css the same way.
document.addEventListener("DOMContentLoaded", () => {
  if (typeof Motion === "undefined") return;
  const { animate, inView, scroll, stagger } = Motion;

  const showAll = () =>
    document
      .querySelectorAll(".fade-up, .hero-intro, .paw-step")
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

  // --- Paw trails: prints appear step by step as the band scrolls through ---
  // Scrubbing back up retracts them, like the dog walked back.
  document.querySelectorAll("[data-paw-trail]").forEach((trail) => {
    const steps = trail.querySelectorAll(".paw-step");
    if (!steps.length) return;
    scroll(
      (progress) => {
        steps.forEach((step, i) => {
          const on = progress >= (i + 1) / (steps.length + 1);
          if (on === (step.dataset.on === "1")) return;
          step.dataset.on = on ? "1" : "0";
          if (on) {
            animate(
              step,
              { opacity: [0, 1], scale: [0.3, 1] },
              { type: "spring", stiffness: 400, damping: 18 }
            );
          } else {
            animate(step, { opacity: 0, scale: 0.3 }, { duration: 0.2 });
          }
        });
      },
      { target: trail, offset: ["start 95%", "end 55%"] }
    );
  });

  // --- Scroll progress bar under the top edge ---
  const progressBar = document.getElementById("scroll-progress");
  if (progressBar) {
    scroll(animate(progressBar, { scaleX: [0, 1] }, { ease: "linear" }));
  }

  // --- Header compresses after scrolling past the hero's first screen ---
  const header = document.getElementById("site-header");
  if (header) {
    const compact = () => header.classList.toggle("scrolled", window.scrollY > 80);
    window.addEventListener("scroll", compact, { passive: true });
    compact();
  }

  // --- Squiggle underlines draw themselves in view ---
  document.querySelectorAll(".squiggle").forEach((svg) => {
    const path = svg.querySelector(".squiggle-path");
    if (!path) return;
    inView(
      svg,
      () => {
        animate(
          path,
          { strokeDashoffset: [1, 0] },
          { duration: 0.8, ease: EASE_OUT, delay: 0.25 }
        );
      },
      { amount: 0.8 }
    );
  });

  // --- Hero shiba leans toward the cursor (fine pointers only) ---
  const heroSection = heroDog && heroDog.closest("section");
  if (heroDog && heroSection && window.matchMedia("(pointer: fine)").matches) {
    heroSection.addEventListener("pointermove", (event) => {
      const rect = heroSection.getBoundingClientRect();
      const dx = (event.clientX - rect.left) / rect.width - 0.5;
      const dy = (event.clientY - rect.top) / rect.height - 0.5;
      animate(
        heroDog,
        { rotate: dx * 3, x: dx * 14, y: dy * 10 },
        { duration: 0.4, ease: "easeOut" }
      );
    });
    heroSection.addEventListener("pointerleave", () => {
      animate(heroDog, { rotate: 0, x: 0, y: 0 }, SPRING);
    });
  }

  // --- Testimonial stars pop in when a slide becomes active (called from Alpine) ---
  window.ppPopStars = (container) => {
    animate(
      container.children,
      { scale: [0, 1], opacity: [0, 1] },
      { type: "spring", stiffness: 400, damping: 15, delay: stagger(0.07) }
    );
  };

  // --- Back-to-top paw + a little paw confetti burst on click ---
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
      const rect = toTop.getBoundingClientRect();
      for (let i = 0; i < 6; i++) {
        const paw = document.createElement("span");
        paw.className = "paw-burst text-lg";
        paw.innerHTML = toTop.innerHTML;
        paw.style.left = `${rect.left + rect.width / 2}px`;
        paw.style.top = `${rect.top}px`;
        document.body.appendChild(paw);
        animate(
          paw,
          {
            x: (Math.random() - 0.5) * 140,
            y: -60 - Math.random() * 90,
            rotate: (Math.random() - 0.5) * 180,
            opacity: [1, 0],
            scale: [1, 0.4],
          },
          { duration: 0.9, ease: "easeOut" }
        ).finished.then(() => paw.remove());
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});
