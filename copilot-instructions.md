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
- Homepage content models: `Service`, `Testimonial`, `FAQ`, `GalleryImage` (all with
  `sort_order`/`is_active`). Rich text fields use `tinymce.models.HTMLField` and render
  with `|safe` inside `.prose-rte` wrappers (admin-authored content only).

## Do not change without approval

- The visual design (colors, fonts, section layout) — it mirrors the Figma file
  (`Hwp2DlF2xLfJlbrSe20cwN`, node 1:5).
- Deployment flow in `scripts/deploy.sh` and the systemd/Nginx assumptions behind it.
- The `config/settings.py` env-driven setup (django-environ, WhiteNoise storage switching).

## Deployment expectations

`scripts/deploy.sh` rsyncs to a server, installs deps, builds, migrates, collects static,
restarts Gunicorn and reloads Nginx. Override via env vars (`REMOTE_HOST`, `SERVER_NAME`, …).
