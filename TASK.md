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

## Done (2026-08-25, individual service pages + real Contact page)

- Each service now has its own detail page at `/services/<slug>/` (`service_detail` view +
  template), built from new Figma frames for Day Care, Puppy Playground, and Birthday
  Parties — unique hero art/heading, unique intro copy, then the same universal pricing
  marquees + CTA (extracted into shared partials `section_pricing_plans.html` and
  `section_cta.html`, also used by the hub `/services/` page). `dog-grooming` has no Figma
  design yet, so it falls back to the generic Meet & Greet copy the other three originally
  shared (`_GENERIC_DETAIL` in views.py) — swap in real content once that design exists.
- Header dropdown, mobile menu, footer Services list, and the "Our Services" cards all link
  to these detail pages now instead of `/services/#anchor`.
- On the `/services/` hub page, the "Our Services" 4-card grid moved to the last content
  section (right before the CTA) so pricing leads, matching the Figma flow.
- Real Contact page built from Figma (`ContactSubmission` model + `ContactForm` +
  `contact()` view) — submissions save to the database and show up in admin
  (read-only, `is_read` triage checkbox), not just a decorative form. Contact info cards
  pull from `SiteSettings` rather than Figma's placeholder address, for consistency with
  the rest of the site.
- Fixed pricing card photo cropping: the marquee's `overflow-hidden` was clipping the dog
  photos that poke above each card — moved the section's top spacing from margin to padding
  so it stays inside the clipped box.
- Removed now-dead `_stub()` view helper and `page_stub.html` (Gallery and Contact both
  have real implementations).
- Fixed the diagonal notch in the footer's top-right corner — the source wave SVGs
  (`footer-wave-1.svg`, `footer-wave-2.svg`) had off-screen-only-safe geometry that became
  visible once stretched to `w-full`; edited the path data directly rather than relying on
  CSS width/overflow tricks.

## Done (2026-08-26, hero banner dog + Grooming detail page)

- Homepage hero dog is now a real cutout (`hero-dog.webp`) with independently layered
  decorations (`hero-dog-blob.webp`, paw/bone/heart/dot assets) behind and around it,
  replacing the old flattened `hero-shiba.webp` box. Positions were measured directly off
  a 1:1 Figma export (node `256:4`) rather than eyeballed.
- Built the real Grooming/Spa detail page (`dog-grooming` in `SERVICE_DETAIL_CONTENT`) from
  its own Figma frame (node `128:111`) — real hero art (`heading-spa.svg`,
  `service-spa-hero.webp`) and intro copy, no longer falling back to `_GENERIC_DETAIL`.
  Verified Day Care, Puppy Playground, and Birthday Parties against their Figma frames
  (`217:2`, `229:1380`, `226:722`) at the same time — all three already matched exactly.
- Added a third intro-heading layout to `service_detail.html` (plain text then a gold
  same-line highlight) for Grooming's "A Fresh **New Look,**" heading — see
  `copilot-instructions.md` for all three layouts.

## Next up

- Booking flow behind the "Book Now" / "Book A Visit" buttons (currently link to Contact).
- Production hardening: real `SECRET_KEY`, `DEBUG=False` env, Nginx/systemd unit files.
