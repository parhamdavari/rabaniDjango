# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Website for Dr. Rabbani's dental clinic (drrabani.com). Django 4.2 project `rabani` with one live app, `website`. The site that is actually published is a **static export** of the Django templates, deployed to GitHub Pages.

## Commands

CI uses Python 3.11, and the pinned requirements are known to install and build on it. The repo has no virtualenv checked in, so create one with 3.11:

```bash
uv venv --python 3.11 .venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

A `.env` file in the repo root is required (it is gitignored). `DEBUG` defaults to `False`; the other four keys have no defaults and must be present, even if empty:

```
SECRET_KEY=dev
DEBUG=True
EMAIL_HOST_USER=dummy@example.com
EMAIL_HOST_PASSWORD=dummy
GOOGLE_ANALYTICS_KEY=
```

`DEBUG=True` selects SQLite (`db.sqlite3`, gitignored). With `DEBUG=False` (and no `BUILD_STATIC` in the process environment) the settings demand `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` for PostgreSQL (and `psycopg2` is not in `requirements.txt`).

```bash
python manage.py migrate
python manage.py runserver            # dynamic site at /en/, /fa/, /ar/ ; admin at /en/admin/
python manage.py check
python manage.py makemigrations --check --dry-run

python build_static.py                # static export -> dist/
cd dist && python -m http.server 8000 # preview the export

python manage.py compilemessages      # after editing any locale/*/LC_MESSAGES/django.po (needs GNU gettext)
```

Tests: every `tests.py` is an empty stub, so `python manage.py test` runs 0 tests. There is no linter or formatter configured. A single test would be run as `python manage.py test website.tests.SomeTestCase.test_method`.

## Architecture: two sites in one repo

The same pages exist twice, and the two copies are maintained by hand.

| | Dynamic Django site | Static export (what is published) |
|---|---|---|
| Templates | `website/templates/*.html` | `website/templates/templates_static/*.html` |
| Rendering | `website/views.py` via `rabani/urls.py` (`i18n_patterns`) | `build_static.py` renders templates directly to `dist/<lang>/<page>.html` |
| Links / assets | `{% url %}`, `{% static %}` | hand-built: `{{ BASE_URL }}/{{ LANGUAGE_CODE }}/page.html`, `{{ BASE_URL }}/static/...` |
| Forms | POST to Django views, `send_mail` | POST to formsubmit.co with a `_next` redirect back to drrabani.com |
| Global context | `website/context_processors.py` | `get_base_context()` in `build_static.py` |
| Deploy | `django.yml` / `main.yml`: SSH deploy on push to `prod`, calling a server-side `scripts/deploy.sh` that is not in this repo | `static-build.yml`: GitHub Pages on push to `main` |

Consequences to keep in mind:

- **A UI or copy change usually has to be made in both template trees.** Changing only `website/templates/` does not affect the published site.
- **Clinic contact details are duplicated** in `website/context_processors.load_global_var` and `build_static.get_base_context()`. The build renders with `loader.get_template(...).render(dict)` and no request, so context processors never run for the static export.
- **Adding a static page** means adding a block to `generate_pages()` in `build_static.py` and setting `PAGE_NAME` in its context; the language switcher in `templates_static/base.html` builds its links from `PAGE_NAME`.
- **`website/views_static.py`, `website/urls_static.py` and `rabani/urls_static.py` are not used by the build** (nothing points `ROOT_URLCONF` at them). Editing them changes nothing in `dist/`.
- **`BUILD_STATIC` only works as a real process environment variable.** `rabani/settings.py` reads it before it loads `.env`, so `BUILD_STATIC=True` inside `.env` is ignored. `build_static.py` sets it itself.
- **The published site has no database content.** CI builds against a fresh, empty SQLite database (the script runs `migrate` itself). Only `templates_static/courses.html` reads the database, so the published courses list is empty. The static home page ignores the slideshow, patient and gallery models: its gallery and before/after images are hardcoded paths under `static/website/images/`. `media/` is committed and copied to `dist/` but is not referenced by the export.
- **The server deploy is currently inert.** `django.yml` and `main.yml` trigger on a `prod` branch that does not exist on origin, so a push to `main` only runs the GitHub Pages build.
- `BASE_URL` (env var) is empty for the custom domain; set it to `/rabaniDjango` only when serving from a github.io subpath. `build_static.py` also writes `CNAME`, `.nojekyll`, a root `index.html` redirecting to `/fa/`, and `404.html`.

## Languages and RTL

- `settings.LANGUAGES` lists `en`, `fa`, `ar`, but the static build only emits `en` and `fa` (`LANGUAGES` in `build_static.py`), with `fa` as the default. Only `locale/fa` is translated; `locale/ar` and `locale/all` have no translated strings, and `locale/en` holds only the `dir` → `ltr` directive.
- The `.po` files carry layout directives as fake translations, not just text: `{% trans 'dir' %}` → `rtl`/`ltr`, `{% trans 'text-align' %}` → `right` (untranslated in `en`, so English pages emit the literal `text-align: text-align`), and `{% trans 'en' %}` → `fa` for `<html lang>`. Direction-sensitive markup should follow the same pattern.
- **Compiled `.mo` files are committed and CI does not run `compilemessages`.** After editing a `.po`, compile and commit the `.mo`, otherwise the published site keeps the old strings.
- Model text is translated with django-parler (`TranslatableModel` / `TranslatedFields` in `website/models.py`, `TranslatableAdmin` in `website/admin.py`); translated fields live in separate `*Translation` tables.

## Frontend assets

- Templates load `static/website/css/style.min.css` and `static/website/js/main.min.js`. There is no build or minify step: `style.css` and `style.min.css` are both edited and committed together by hand. Changing only the unminified file has no visible effect.
- `static/website/scss/` is the original theme source and is not compiled by anything in this repo.
- Edit files under `static/`, never `staticfiles/`. `staticfiles/` is `collectstatic` output that is gitignored but still has files tracked from earlier commits.

## Dormant code

`blog/` and `AccessControl/` contain models, views and templates but are not in `INSTALLED_APPS` and are not routed. `website/templates/blog.html` belongs to that unused blog. Treat them as inactive unless asked to revive them.
