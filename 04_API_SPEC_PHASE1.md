# EduPrep Phase 1 API

Base: /api/v1

## Health
GET /health

## Exams
GET /exams
GET /exams/{exam_id}

## Subjects
GET /subjects?exam_id={id}
GET /subjects/{subject_id}

## Topics
GET /subjects/{subject_id}/topics

## Questions
GET /questions
GET /questions/{question_id}

Filters: exam_id, subject_id, topic_id, limit, offset.

Do not return correct-answer fields before submission.

## Practice
POST /practice
GET /practice/{session_id}
POST /practice/{session_id}/attempt
POST /practice/{session_id}/complete

Attempt request:
{
  "question_id": "uuid",
  "selected_option": "B",
  "time_spent_seconds": 18
}

Backend determines correctness.

## Progress
GET /progress
GET /progress/subjects
GET /progress/topics

## Profile
GET /profile
PATCH /profile

## Future only
/admin/content/import
/admin/content/review
/admin/content/publish
/ai/explain
/ai/hint
/ai/teach

Do not build future endpoints unless explicitly requested.
