# EduPrep Phase 1 Architecture

## High level
Flutter Mobile
↓ HTTPS
FastAPI Backend
↓
Supabase PostgreSQL/Auth

Current question source:
Seeded database content

Future:
ALOC → Content Adapter → Database

## Frontend
Flutter/Dart with feature-based structure:
lib/core
lib/features/auth
lib/features/onboarding
lib/features/home
lib/features/exams
lib/features/subjects
lib/features/practice
lib/features/progress
lib/features/profile
lib/shared

UI must use repositories/services and must not know the external provider.

## Backend
FastAPI/Python:
app/main.py
app/config.py
app/api/
app/models/
app/schemas/
app/repositories/
app/services/practice/
app/services/progress/
app/services/content/
app/database/
app/tests/

## Content abstraction
Create a QuestionRepository/ContentProvider abstraction.

Phase 1: DatabaseQuestionProvider.
Later: ALOCProvider → importer/normaliser → database.

Flutter must never call ALOC directly.

## Answer security
Client sends question_id, selected_option and session_id. Backend loads authoritative answer, calculates correctness, records attempt, updates progress and returns feedback.

## Environment
Backend secrets:
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
Future: ALOC_API_KEY and OPENAI_API_KEY

Never expose privileged credentials to Flutter.

## Deployment
Use managed services. Recommended initial setup: Supabase + Render/Railway for FastAPI + Android Flutter build + GitHub.

Do not introduce Kubernetes, microservices or complex infrastructure in Phase 1.
