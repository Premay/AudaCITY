# Implementation Status

## Architecture change (this revision)

The project was originally a FastAPI backend intended to be called by a
separate Flutter mobile app. It was being deployed to Streamlit Community
Cloud, which only runs Streamlit scripts and cannot expose a callable HTTP
API — so the FastAPI routes were never reachable there, and a Flutter
client could not have used this deployment regardless of how the repo was
structured.

This revision drops the FastAPI/HTTP layer entirely and rebuilds the same
functionality as a self-contained Streamlit app that talks to Supabase
directly, in-process. **Flutter can no longer use this deployment as a
backend** — if a separate mobile client is still wanted later, it needs its
own FastAPI (or similar) service deployed on a host that runs ASGI apps
(e.g. Render, Railway, Fly.io), which is a different piece of work from
this app.

The repo is also intentionally flat — one file per concern, no
subfolders — including the app's Catalogue and Profile views, which are
switched via a sidebar menu inside `streamlit_app.py` instead of a
Streamlit `pages/` folder.

## Completed (Streamlit app)

- `streamlit_app.py`: login, registration, password-reset forms, and
  (once signed in) a sidebar-switched Catalogue and Profile view — all in
  one script.
- Session handling via `st.session_state` (access token + email), with
  logout.
- Catalogue view: browse exams and subjects, drill into a subject's
  topics.
- Profile view: view and edit full name and class level.
- `supabase_client.py`: synchronous Supabase Auth + PostgREST client,
  ported 1:1 from the original FastAPI service layer's behavior.
- `config.py`: reads Supabase URL/anon key from Streamlit Secrets (Cloud)
  or `.env` (local dev).
- Unit tests for `SupabaseClient`'s configuration and header handling
  (`test_supabase_client.py`).
- Supabase Postgres migration (unchanged): core data model, RLS policies,
  initial JAMB/WAEC/subject seed records (`202608170001_initial_schema.sql`).

## Deliberately not implemented

- Flutter application and screens — out of scope for this Streamlit app.
- ALOC adapter, imports, and review/publishing workflow.
- Question browsing, practice, results, and progress tracking.
- AI, payments, gamification, admin UI, parent, teacher, and offline
  features.

## Next step

Add a practice/question flow to the Streamlit app against the seeded
catalogue data, or start a separate FastAPI service (on a proper ASGI host)
if a Flutter client is still wanted alongside this web app.
