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

## Done (2026-08-18, dynamic Services + Gallery + admin expansion)

- Services page now shows the 4 Service cards (shared `partials/section_services.html`,
  reused on Home too) above the pricing plans, each card anchored by `id="{{ slug }}"`.
- Header "Services" nav item is a hover/focus dropdown (pure CSS `group`, no JS) listing
  the 4 services, linking to `/services/#<slug>`. Same list duplicated in the mobile menu
  and the footer's Services column.
- Pricing plans moved from hardcoded Python dicts to a `PricingPlan` model (admin-editable:
  name, dog_count 1/2, price, period, tone, feature list, photo). Both plan rows render as
  auto-scrolling marquees (pause on hover) instead of a fixed grid, so admins can add more
  plans without breaking layout — scroll speed scales with plan count.
- `TeamMember` model replaces the hardcoded About page bios (rich-text via TinyMCE).
- `SiteSettings` singleton model (phone, email, address, hours, Facebook/Instagram) — the
  footer and social icons now read from it instead of hardcoded text/dead `#` links.
  Injected everywhere via a new context processor (`website.context_processors.site_globals`,
  also supplies `nav_services` for the dropdown/footer/mobile menu).
- Gallery page is real now (masonry grid of all active `GalleryImage`s), not a stub.
- `seed_demo` extended to seed all of the above.

## Next up

- Real pages for Contact (currently a stub sharing `page_stub.html`).
- Booking flow behind the "Book Now" / "Book A Visit" buttons (currently link to contact stub).
- Production hardening: real `SECRET_KEY`, `DEBUG=False` env, Nginx/systemd unit files.
- Consider individual detail pages per service (currently anchor-links on one Services page).
