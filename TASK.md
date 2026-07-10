# Active work

## Done (2026-07-10)

- Project bootstrapped: Django 5.2 + Tailwind v4 + Alpine + Motion + Lucide fragments.
- Homepage implemented from the Figma design (hero, story, services, features, testimonials,
  gallery, CTA, FAQ, footer) with assets exported from Figma into `website/static/img/`.
- Admin content models (Service, Testimonial, FAQ, GalleryImage) with TinyMCE rich text.
- `seed_demo` management command, pytest suite, Ruff/djLint/pre-commit, deploy script.

## Done (2026-07-10, animation pass)

- Creative animation layer: staged hero intro (Motion springs + line stagger), scroll-linked
  parallax (`data-parallax`), staggered section reveals (`data-stagger`), spring pop-ins
  (`data-pop`), infinite marquee gallery rows (CSS, pause on hover), animated FAQ accordion
  (grid-rows collapse), auto-playing testimonial carousel with cross-fade (Alpine transitions),
  card hover lift/zoom, floating paw/bone/heart graphics, back-to-top paw button.
- All motion honors `prefers-reduced-motion` (JS bails out + CSS gates keyframes).

## Next up

- Real pages for About / Services / Gallery / Contact (currently stubs sharing `page_stub.html`).
- Booking flow behind the "Book Now" / "Book A Visit" buttons (currently link to contact stub).
- Production hardening: real `SECRET_KEY`, `DEBUG=False` env, Nginx/systemd unit files.
