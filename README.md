# EduPrep

EduPrep is a mobile-first Nigerian WAEC and JAMB preparation platform.

This repository currently contains the Phase 0 backend and database foundation. The Flutter application, question-practice flow, and ALOC import workflow are intentionally not implemented yet.

## Structure

- `backend/` — FastAPI service and automated tests.
- `supabase/migrations/` — PostgreSQL schema and Row Level Security policies for Supabase.
- `docs/` — implementation notes and current scope status.

## Local backend setup

Run these commands in PowerShell from this folder:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to see the API documentation. The health endpoint is available at `GET /api/v1/health`.

Configure Supabase email/password authentication and set the Supabase project URL and anon key in `backend/.env`. The backend forwards authentication requests to Supabase; Flutter calls these FastAPI endpoints and does not need database credentials.

Do not put real keys in `.env.example` or commit a `.env` file.

## Database setup

Create a Supabase project, then run `supabase/migrations/202608170001_initial_schema.sql` using the Supabase SQL Editor or your migration workflow. It creates the core tables, indexes, initial exam/subject records, and Row Level Security policies.

The service-role key is for the backend only. Flutter must call FastAPI and must never call ALOC directly.
