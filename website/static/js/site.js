// Scroll-reveal animations via Motion (vendored UMD bundle exposing window.Motion).
document.addEventListener("DOMContentLoaded", () => {
  if (typeof Motion === "undefined") return;
  const { animate, inView } = Motion;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll(".fade-up").forEach((el) => (el.style.opacity = 1));
    return;
  }

  inView(
    ".fade-up",
    (el) => {
      animate(el, { opacity: [0, 1], y: [24, 0] }, { duration: 0.5, ease: "easeOut" });
    },
    { amount: 0.2 }
  );
});
