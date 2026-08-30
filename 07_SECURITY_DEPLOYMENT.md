# EduPrep Phase 1 Security and Deployment

## Secrets
Never commit .env, API tokens, private keys, Supabase service-role keys, OpenAI keys or ALOC keys.

Use local .env and deployment-platform secret/environment-variable settings.

## Backend variables
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

Future:
ALOC_API_KEY=
OPENAI_API_KEY=

## Git
Before pushing:
- verify .env is ignored
- search repository for keys/tokens
- verify documentation contains no real credentials

## Database
Enable Row Level Security on user-owned tables.

## Backend
Validate authentication, input and ownership. Return structured errors. Never expose stack traces.

## Deployment sequence
1. Create GitHub repository.
2. Create Supabase project.
3. Apply schema/migrations.
4. Seed demo content.
5. Configure backend environment variables.
6. Deploy FastAPI.
7. Verify /health.
8. Configure Flutter with public client/backend settings.
9. Test registration, practice, results and progress.
10. Build Android release.

## Production checklist
- No secrets in Git
- Auth works
- RLS enabled
- Seed content works
- Server-side correctness
- Attempts persist
- Progress persists
- Health endpoint works
- Error handling works
- Android build succeeds
- Privacy/legal review before broad public launch
