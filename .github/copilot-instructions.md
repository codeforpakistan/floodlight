# Copilot Instructions for Floodlight Django Project

## Project Overview
Floodlight is a Django web application scaffolded for local development with SQLite and intended for deployment on DigitalOcean App Platform (PostgreSQL in production). The codebase follows standard Django conventions with a single main project (`floodlight`) and apps (e.g., `core`).

## Architecture & Data Flow
- The main Django project is in the `floodlight/` directory.
- Apps are created in the root (e.g., `core/`).
- Data flows through Django ORM models, views, and templates. SQLite is used for local development; switch to PostgreSQL for production.
- Static files are served from the `static/` directory. Media files should be configured as needed.

## Developer Workflows

**Activate environment:** Always run `.venv/Scripts/Activate.ps1` before any script or Django command.
**Run server:** `python manage.py runserver`
**Create app:** `python manage.py startapp <appname>`
**Migrations:**
  - Make: `python manage.py makemigrations`
  - Apply: `python manage.py migrate`
**Tests:** `python manage.py test`
**Install dependencies:** Use `uv pip install <package>` or update `pyproject.toml`.

## Project-Specific Patterns
- Use SQLite for development (`settings.py`), PostgreSQL for production (update `DATABASES` in `settings.py`).
- All new apps must be added to `INSTALLED_APPS` in `settings.py`.
- For DigitalOcean deployment, ensure `psycopg2-binary` is installed and database settings are production-ready.
- Secret keys and sensitive settings should be managed via environment variables in production.

## Integration Points
- External dependencies are managed via `uv` and `pyproject.toml`.
- Database integration: SQLite (dev), PostgreSQL (prod).
- Static/media file handling should be configured for cloud deployment.

## Key Files & Directories
- `floodlight/settings.py`: Main configuration, database, apps, static/media settings
- `manage.py`: Entrypoint for Django commands
- `pyproject.toml`: Python dependencies
- `.venv/`: Virtual environment (if present)
- `core/`: Example app directory

## Example Patterns
- To add a new model, create it in `core/models.py`, run migrations, and register with admin if needed.
- To add a view, use `core/views.py` and map it in `core/urls.py` (add to project `urls.py`).
- For custom management commands, add to `core/management/commands/`.

---

If any section is unclear or missing, please provide feedback to improve these instructions for future AI agents.
