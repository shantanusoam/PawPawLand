# Paw Paw Land

Marketing site for Paw Paw Land — a dog daycare, grooming, puppy playground and birthday party
business. Django 5.2 + Tailwind CSS v4, with homepage content (services, testimonials, FAQs,
gallery) managed from the Django admin using a TinyMCE rich text editor.

Design source: [Paw Paw Land Figma file](https://www.figma.com/design/Hwp2DlF2xLfJlbrSe20cwN/Paw-Paw-Land?node-id=1-5)
(fonts: Fredoka + Poppins; palette navy `#2A2860`, gold `#FFC93C`, coral `#FF7A59`, cream `#FFFCF6`).

## Stack

- Python 3.12, Django 5.2, django-environ, WhiteNoise, Gunicorn
- Tailwind CSS v4 via `@tailwindcss/cli`, Alpine.js, Motion (scroll animations), Lucide (icon fragments)
- django-tinymce for rich text editing in the admin
- Pytest + pytest-django, Ruff, djLint, pre-commit

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
cp .env.example .env

npm run build
python manage.py migrate
python manage.py seed_demo          # demo content matching the Figma design
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8007
```

For CSS development, run in a second terminal:

```bash
npm run dev
```

## Everyday commands

```bash
pytest                                          # tests
ruff check . && ruff format .                   # lint + format Python
djlint website/templates --reformat             # format Django templates
pre-commit install                              # once, to enable git hooks
```

## Content editing

Log into `/admin/`. Services, Testimonials, FAQs and Gallery images drive the homepage.
Rich text fields (service description, testimonial quote, FAQ answer) use TinyMCE.
Each model has `sort_order` and `is_active` to reorder/hide entries without deleting.

## Deployment

```bash
scripts/deploy.sh
# or with overrides:
REMOTE_HOST=example.com SERVER_NAME=app.example.com scripts/deploy.sh
```

The script rsyncs the code, installs Python/Node dependencies, builds assets, runs migrations,
collects static files, restarts Gunicorn (`systemctl restart pawpawland`) and reloads Nginx.
Configure `REMOTE_USER`, `REMOTE_DIR`, `SERVICE_NAME` via environment variables as needed.
