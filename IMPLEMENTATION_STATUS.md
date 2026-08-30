# Implementation Status

## Completed foundation

- FastAPI application shell with server-side configuration loading, a versioned `/api/v1` route, predictable errors, and a health check.
- FastAPI-mediated registration, login, logout, password-reset, and authenticated profile endpoints using Supabase Auth.
- A database trigger that creates the public profile record whenever Supabase Auth creates a user.
- Authenticated, read-only FastAPI endpoints for exams, subjects, and topics, using Supabase Row Level Security.
- Supabase PostgreSQL migration for the documented core data model.
- Initial JAMB, WAEC, and five priority-subject seed records.
- Row Level Security for user-owned profile, session, attempt, and progress data.
- Initial test for the health endpoint.

## Deliberately not implemented

- Flutter application and screens.
- ALOC adapter, imports, review/publishing workflow, or any external API calls.
- Question browsing, practice, results, and progress endpoints.
- AI, payments, gamification, admin UI, parent, teacher, and offline features.

## Next step

Create the Flutter application shell and implement the login, registration, exam, subject, and topic selection screens against the existing FastAPI endpoints.
