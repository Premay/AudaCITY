# EduPrep

EduPrep is a Nigerian WAEC and JAMB exam-preparation web app, built as a
**Streamlit app** that talks to Supabase (Auth + Postgres) directly.

> This repo previously contained a separate FastAPI backend meant to be
> called by a Flutter mobile app. That HTTP API has been retired — Streamlit
> Community Cloud only runs Streamlit scripts, it does not expose a
> callable REST API. All the same functionality (login, registration,
> catalogue browsing, profile editing) now lives directly in this Streamlit
> app, calling Supabase in-process. See `IMPLEMENTATION_STATUS.md` for the
> full before/after.

## Structure

Every file sits at the repo root — no subfolders, so uploading to GitHub
is just dragging all of these in at once:

| File | Purpose |
|---|---|
| `streamlit_app.py` | Entry point: login/register/reset, plus a sidebar-switched Catalogue and Profile view once signed in |
| `config.py` | Reads Supabase settings from Streamlit Secrets or `.env` |
| `supabase_client.py` | Supabase Auth + PostgREST calls, in-process |
| `test_supabase_client.py` | Unit tests for the client |
| `202608170001_initial_schema.sql` | Database schema — run manually in the Supabase SQL Editor |
| `requirements.txt` | Pip dependencies (Streamlit Cloud reads this) |
| `requirements-dev.txt` | + pytest, for local test runs |
| `.env.example` | Local dev config template |
| `.gitignore` | Keeps `.env` and secrets out of git |
| `IMPLEMENTATION_STATUS.md` | Current scope and what's not built yet |

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env             # then fill in SUPABASE_URL and SUPABASE_ANON_KEY
streamlit run streamlit_app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

Run tests with:

```bash
pytest
```

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub — every file at root, no folders needed.
2. On [share.streamlit.io](https://share.streamlit.io), create a new app
   pointing at this repo, branch, and `streamlit_app.py` as the entry file.
3. In the app's **Settings > Secrets**, paste:
   ```toml
   SUPABASE_URL = "your-project-url"
   SUPABASE_ANON_KEY = "your-anon-key"
   ```
   Never commit those real values to the repo.
4. Deploy. Streamlit Cloud installs from `requirements.txt` automatically —
   there's no `pyproject.toml` in this repo, so there's no ambiguity about
   which package manager it should use.

## Database setup

Unchanged: create a Supabase project, then run
`202608170001_initial_schema.sql` via the Supabase SQL Editor or your
migration workflow. It creates the core tables, indexes, initial
exam/subject records, and Row Level Security policies.

Only the anon key is used by this app (never the service-role key) — every
request runs as the logged-in user, enforced by Supabase Row Level
Security.
