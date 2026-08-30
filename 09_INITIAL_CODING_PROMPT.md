# Initial AI Coding Prompt — EduPrep Phase 1

You are the lead engineer helping deploy EduPrep Phase 1.

Read these files first:
- 00_SOURCE_OF_TRUTH.md
- 01_PRD_PHASE1.md
- 02_ARCHITECTURE_PHASE1.md
- 03_DATABASE_SCHEMA_PHASE1.md
- 04_API_SPEC_PHASE1.md
- 06_DESIGN_SYSTEM_PHASE1.md
- 07_SECURITY_DEPLOYMENT.md
- 08_AI_CODING_RULES.md

Important:
ALOC has NOT been integrated. Do not require or implement it for the initial deployment.

The immediate goal is a usable deployed application using seeded/demo questions.

Before modifying files:
1. Inspect the repository.
2. Identify the current project structure and stack.
3. Identify what Phase 1 already implements.
4. Identify blockers.
5. Give me a short implementation plan.
6. Do not modify files until the plan is reported.

Required architecture:
Flutter → FastAPI → Supabase

Current content:
Seed data → Supabase → FastAPI → Flutter

Future:
ALOC → Content Adapter → Supabase → FastAPI → Flutter

Do not put ALOC credentials in the codebase.

Work incrementally and do not implement Phase 2 features.
