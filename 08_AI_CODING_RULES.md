# EduPrep AI Coding Rules

Read 00_SOURCE_OF_TRUTH.md before changing the project.

## Current task
Deploy Phase 1 using seeded database questions.

Do NOT require ALOC integration.

## Before coding
1. Inspect the repository.
2. Identify the existing frontend/backend/database.
3. Identify what already works.
4. Compare it to the source-of-truth documents.
5. Propose the smallest next implementation step.

## Rules
- Do not rewrite unrelated code.
- Do not add unnecessary frameworks.
- Do not add microservices.
- Do not add AI, payments or advanced gamification in Phase 1.
- Do not integrate ALOC unless explicitly requested.
- Never expose secrets.
- Never call ALOC/OpenAI directly from Flutter.
- Never trust client-provided correctness.
- Keep question source behind a repository/provider abstraction.

## After each task
Report:
1. files changed
2. what was implemented
3. tests/commands run
4. result
5. remaining work

The owner is not a professional developer. Give copy/paste-friendly commands, say where to run them, and explain successful output/errors simply.
