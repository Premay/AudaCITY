# EduPrep Phase 1 Database Schema

## profiles
id, full_name, class_level, preferred_exam_id, created_at, updated_at

## exams
id, name, code, description, created_at

Initial: JAMB, WAEC.

## subjects
id, name, code, created_at

Initial: English Language, Mathematics, Physics, Chemistry, Biology.

## topics
id, subject_id, name, description, created_at

## content_sources
id, name, source_type, source_url, external_reference, licence_status, notes, created_at, updated_at

Statuses: PENDING_VERIFICATION, APPROVED, RESTRICTED, REJECTED.

Phase 1 seed source: DEMO_SEED.

## questions
id, exam_id, subject_id, topic_id, source_id, external_id, question_text, question_type, difficulty, year, image_url, status, created_at, updated_at

Statuses: DRAFT, PENDING_REVIEW, APPROVED, PUBLISHED, ARCHIVED.

Only PUBLISHED questions are available to normal students.

## question_options
id, question_id, option_key, option_text, is_correct

is_correct is server-only.

## explanations
id, question_id, explanation_text, source_type, review_status, created_at, updated_at

## practice_sessions
id, user_id, exam_id, subject_id, topic_id, question_count, score, completed, started_at, completed_at

## attempts
id, user_id, session_id, question_id, selected_option, is_correct, time_spent_seconds, created_at

## student_progress
id, user_id, subject_id, topic_id, questions_attempted, questions_correct, accuracy, last_attempted_at, updated_at

## Security
Use Row Level Security. Students access only permitted records belonging to their account. Historical attempts should not be freely editable by the client.
