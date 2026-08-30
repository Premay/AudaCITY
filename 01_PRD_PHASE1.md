# EduPrep Phase 1 PRD

## Product
EduPrep — WAEC and JAMB preparation for Nigerian secondary-school students.

## Objective
Get a functional first version into users' hands while keeping the architecture ready for future API content, AI, adaptive learning and offline improvements.

## User stories
- I can create an account and sign in.
- I can choose JAMB or WAEC.
- I can select a subject.
- I can select a topic or mixed practice.
- I can answer MCQs.
- I can see whether my answer is correct.
- I can read an explanation.
- I can complete a session and see my score.
- I can return later and see my progress.

## Required screens
1. Splash/loading
2. Login
3. Registration
4. Password reset
5. Onboarding/profile
6. Home
7. Exam selection
8. Subject selection
9. Topic selection
10. Practice/question
11. Answer feedback
12. Results
13. Progress
14. Profile/settings

## Question behaviour
One question at a time. The student submits an option. The backend determines correctness and returns feedback/explanation. Correct answers must not be exposed before submission.

## Results
Show total questions, correct, incorrect, percentage score and time spent where available.

## Progress
Show total attempted, total correct, overall accuracy, recent sessions and subject accuracy.

## Phase 1 content
Use seeded data. It must flow through the same internal question service that future ALOC-imported content will use.

## Out of scope
ALOC/SdashAPI integration, AI tutor, adaptive learning, offline mode, payments, parent/teacher portals, school management, leaderboards, advanced gamification, full CMS and voice/video learning.

## Acceptance
Authentication works; seeded questions load; answers are server-validated; explanations work; results and attempts persist; progress persists across sessions; mobile UI works; deployment is documented; secrets are not in source control.
