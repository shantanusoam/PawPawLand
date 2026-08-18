# Repo rules for AI assistants

## Run the app

```bash
source .venv/bin/activate
npm run build                       # or `npm run dev` in a second terminal while editing CSS
python manage.py migrate
python manage.py runserver 127.0.0.1:8007
```

`python manage.py seed_demo` loads demo content (idempotent). Admin lives at `/admin/`.

## Tests and quality gates

```bash
pytest
ruff check . && ruff format .
djlint website/templates --lint
```

Run all three before considering a change done. Tests live under `tests/website/`, not in the app.

## CSS

- Source of truth is `website/static/src/styles.css` (Tailwind v4, CSS-first `@theme` config).
- `website/static/css/site.css` is **generated** — never edit it; rebuild with `npm run build`.
- Design tokens (colors `navy/gold/coral/ink/cream/…`, fonts `font-display`=Fredoka,
  `font-sans`=Poppins) come from the Figma design. Use the tokens, not raw hex, in templates.
- Tailwind v4 cannot `@apply` custom component classes — compose with shared selectors instead.

## Templates and conventions

- Django templates under `website/templates/website/`; all pages extend `base.html`.
- Icons are inline SVG fragments in `website/templates/website/icons/` — include them,
  don't add icon JS libraries or CDN links.
- Interactivity uses Alpine.js (vendored `alpine.min.js`); scroll animations use Motion
  (vendored `motion.min.js`, exposed as `window.Motion`) wired up in `website/static/js/site.js`.
- Content models: `Service`, `Testimonial`, `FAQ`, `GalleryImage`, `PricingPlan`,
  `TeamMember` (all with `sort_order`/`is_active`), plus the `SiteSettings` singleton
  (`SiteSettings.load()`, pk always 1). Rich text fields use `tinymce.models.HTMLField`
  and render with `|safe` inside `.prose-rte` wrappers (admin-authored content only).
- `website.context_processors.site_globals` injects `nav_services` and `site_settings`
  into every template's context (registered in `TEMPLATES.OPTIONS.context_processors`) —
  don't re-query these in individual views.
- Sections shared between pages live as standalone partials
  (`partials/section_our_story.html`, `section_why_dogs_love.html`, `section_gallery.html`,
  `section_services.html`) — include them rather than duplicating markup across templates.
- Auto-scrolling rows (`.marquee`/`.marquee-track`/`.marquee-copy`, pause on hover) are used
  for the photo gallery and the pricing plan rows so admins can add more items without
  breaking the layout. Scroll speed is set per-instance via an inline
  `style="--pp-marquee-duration: …s"` (djlint's H021 is ignored project-wide for this reason
  — Tailwind's build-time class scanning can't express a per-request dynamic value).

## Do not change without approval

- The visual design (colors, fonts, section layout) — it mirrors the Figma file
  (`Hwp2DlF2xLfJlbrSe20cwN`, node 1:5).
- Deployment flow in `scripts/deploy.sh` and the systemd/Nginx assumptions behind it.
- The `config/settings.py` env-driven setup (django-environ, WhiteNoise storage switching).

## Deployment expectations

`scripts/deploy.sh` rsyncs to a server, installs deps, builds, migrates, collects static,
restarts Gunicorn and reloads Nginx. Override via env vars (`REMOTE_HOST`, `SERVER_NAME`, …).
