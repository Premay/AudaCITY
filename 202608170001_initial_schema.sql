-- EduPrep Phase 0 foundation. Apply through the Supabase SQL Editor or migration tool.
-- This migration stores verified content and student-owned learning data.

create extension if not exists pgcrypto;

create type public.licence_status as enum (
  'PENDING_VERIFICATION', 'APPROVED', 'RESTRICTED', 'REJECTED'
);
create type public.question_status as enum (
  'DRAFT', 'PENDING_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED'
);
create type public.explanation_source_type as enum ('PROVIDER', 'EDUPREP', 'AI');
create type public.review_status as enum ('PENDING_REVIEW', 'APPROVED', 'REJECTED');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  email text not null,
  class_level text,
  preferred_exam uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.exams (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  code text not null unique,
  description text,
  created_at timestamptz not null default now()
);

create table public.subjects (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  code text not null unique,
  created_at timestamptz not null default now()
);

alter table public.profiles
  add constraint profiles_preferred_exam_fkey
  foreign key (preferred_exam) references public.exams(id) on delete set null;

create table public.topics (
  id uuid primary key default gen_random_uuid(),
  subject_id uuid not null references public.subjects(id) on delete cascade,
  name text not null,
  description text,
  created_at timestamptz not null default now(),
  unique (subject_id, name)
);

create table public.content_sources (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  source_type text not null,
  source_url text,
  licence_status public.licence_status not null default 'PENDING_VERIFICATION',
  licence_reference text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.questions (
  id uuid primary key default gen_random_uuid(),
  exam_id uuid not null references public.exams(id),
  subject_id uuid not null references public.subjects(id),
  topic_id uuid references public.topics(id) on delete set null,
  source_id uuid not null references public.content_sources(id),
  external_id text,
  question_text text not null,
  question_type text not null default 'MCQ',
  difficulty text,
  year integer check (year between 1900 and 2100),
  image_url text,
  status public.question_status not null default 'DRAFT',
  imported_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (source_id, external_id)
);

create table public.question_options (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null references public.questions(id) on delete cascade,
  option_key text not null,
  option_text text not null,
  is_correct boolean not null default false,
  unique (question_id, option_key)
);

create table public.explanations (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null unique references public.questions(id) on delete cascade,
  explanation_text text not null,
  source_type public.explanation_source_type not null,
  review_status public.review_status not null default 'PENDING_REVIEW',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.practice_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  exam_id uuid not null references public.exams(id),
  subject_id uuid not null references public.subjects(id),
  topic_id uuid references public.topics(id) on delete set null,
  question_count integer not null check (question_count > 0),
  score integer not null default 0 check (score >= 0),
  completed boolean not null default false,
  started_at timestamptz not null default now(),
  completed_at timestamptz
);

create table public.attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  session_id uuid references public.practice_sessions(id) on delete set null,
  question_id uuid not null references public.questions(id),
  selected_option text not null,
  is_correct boolean not null,
  time_spent_seconds integer check (time_spent_seconds >= 0),
  created_at timestamptz not null default now(),
  unique (session_id, question_id)
);

create table public.student_progress (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  subject_id uuid not null references public.subjects(id),
  topic_id uuid references public.topics(id) on delete set null,
  questions_attempted integer not null default 0 check (questions_attempted >= 0),
  questions_correct integer not null default 0 check (questions_correct >= 0 and questions_correct <= questions_attempted),
  accuracy numeric(5,2) not null default 0 check (accuracy between 0 and 100),
  last_attempted_at timestamptz,
  updated_at timestamptz not null default now(),
  unique nulls not distinct (user_id, subject_id, topic_id)
);

create index questions_exam_id_idx on public.questions (exam_id);
create index questions_subject_id_idx on public.questions (subject_id);
create index questions_topic_id_idx on public.questions (topic_id);
create index questions_source_id_idx on public.questions (source_id);
create index questions_external_id_idx on public.questions (external_id);
create index attempts_user_id_idx on public.attempts (user_id);
create index attempts_question_id_idx on public.attempts (question_id);
create index attempts_session_id_idx on public.attempts (session_id);
create index student_progress_user_id_idx on public.student_progress (user_id);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at before update on public.profiles
for each row execute function public.set_updated_at();
create trigger content_sources_set_updated_at before update on public.content_sources
for each row execute function public.set_updated_at();
create trigger questions_set_updated_at before update on public.questions
for each row execute function public.set_updated_at();
create trigger explanations_set_updated_at before update on public.explanations
for each row execute function public.set_updated_at();
create trigger student_progress_set_updated_at before update on public.student_progress
for each row execute function public.set_updated_at();

-- Supabase Auth owns credentials. This trigger creates the matching public profile
-- without sending a service-role key to either FastAPI clients or Flutter.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, full_name, class_level)
  values (
    new.id,
    new.email,
    nullif(new.raw_user_meta_data ->> 'full_name', ''),
    nullif(new.raw_user_meta_data ->> 'class_level', '')
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Core reference records. Topics are added only after reliable classification.
insert into public.exams (name, code, description) values
  ('Joint Admissions and Matriculation Board', 'JAMB', 'Unified Tertiary Matriculation Examination'),
  ('West African Examinations Council', 'WAEC', 'West African Senior School Certificate Examination')
on conflict (code) do nothing;

insert into public.subjects (name, code) values
  ('English Language', 'ENGLISH'),
  ('Mathematics', 'MATHEMATICS'),
  ('Physics', 'PHYSICS'),
  ('Chemistry', 'CHEMISTRY'),
  ('Biology', 'BIOLOGY')
on conflict (code) do nothing;

-- User data is protected even though Flutter will use FastAPI rather than direct SQL.
alter table public.profiles enable row level security;
alter table public.exams enable row level security;
alter table public.subjects enable row level security;
alter table public.topics enable row level security;
alter table public.content_sources enable row level security;
alter table public.questions enable row level security;
alter table public.question_options enable row level security;
alter table public.explanations enable row level security;
alter table public.practice_sessions enable row level security;
alter table public.attempts enable row level security;
alter table public.student_progress enable row level security;

create policy "Users can view their own profile" on public.profiles
  for select using (auth.uid() = id);
create policy "Users can update their own profile" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);
create policy "Authenticated users can view exams" on public.exams
  for select to authenticated using (true);
create policy "Authenticated users can view subjects" on public.subjects
  for select to authenticated using (true);
create policy "Authenticated users can view topics" on public.topics
  for select to authenticated using (true);
create policy "Users can view their own practice sessions" on public.practice_sessions
  for select using (auth.uid() = user_id);
create policy "Users can view their own attempts" on public.attempts
  for select using (auth.uid() = user_id);
create policy "Users can view their own progress" on public.student_progress
  for select using (auth.uid() = user_id);

-- Student writes to attempts, sessions and progress will be performed by FastAPI.
-- The backend validates answers and uses a service-role connection; it is never exposed to Flutter.
-- Questions, options, explanations, and source records have no client-side select policy.
-- This prevents exposing correct options and keeps the FastAPI boundary mandatory.
