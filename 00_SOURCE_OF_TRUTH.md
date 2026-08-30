# EduPrep Phase 1 — Source of Truth

EduPrep is a mobile-first Nigerian EdTech app for secondary-school students preparing for WAEC/WASSCE and JAMB/UTME.

## Phase 1 goal
Deploy a usable first version BEFORE integrating the past-question API.

The deployed app must use seeded/demo questions so API integration can be added later without redesigning the product.

## Required student journey
Register/Login → Choose exam → Choose subject → Choose topic → Start practice → Answer → Submit → See result → Read explanation → Continue → Finish → See score → See saved progress.

## Phase 1 includes
- Authentication
- Student profile
- JAMB and WAEC selection
- English, Mathematics, Physics, Chemistry and Biology
- Subject/topic browsing
- Multiple-choice practice
- Server-side answer validation
- Explanations
- Session results
- Persistent attempts
- Basic progress dashboard
- Mobile-first UI
- Deployment
- Environment-variable configuration
- Seed/demo question data

## Phase 1 does NOT depend on ALOC
ALOC is not integrated yet. Do not block deployment waiting for it.

Current:
Seeded Dataset → Database → FastAPI → Flutter

Future:
ALOC → Content Adapter → EduPrep Database → FastAPI → Flutter

## Preferred stack
- Flutter + Dart
- FastAPI + Python
- Supabase PostgreSQL
- Supabase Auth
- Supabase Storage when needed
- Next.js + TypeScript for future admin
- OpenAI only in a later AI phase

## Non-negotiable security
- Never put ALOC/OpenAI/database service-role secrets in Flutter.
- Never commit .env files.
- Correct answers are validated server-side.
- Students cannot modify historical attempts or question correctness.
- Use Row Level Security for user-owned data.

## Content integrity
Past questions must ultimately come from credible/authorised sources. API accessibility does not automatically grant redistribution rights.

Retain source, external ID, year, licensing/usage status and review status. Only approved/published content should be presented as official past-question content.

Seed/demo questions must be clearly labelled as demo/seed content unless their source and rights are verified.

## Phase 1 success
A user can use the deployed app, create an account, practise seeded questions, receive correct feedback/explanations, complete a session, and return later to see saved progress.

This document is the Phase 1 source of truth.
