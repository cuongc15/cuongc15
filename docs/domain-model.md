# Domain model & phân loại class

## Core entities

### User
- `id`, `email`, `password_hash`, `full_name`, `phone`, `status`, `created_at`.

### Role
- `id`, `name`.
- Gợi ý role: `admin`, `teacher`, `student`, `parent`.

### UserRole
- Quan hệ N-N giữa User và Role.

### Organization
- `id`, `name`, `org_type`, `address`.

### ClassRoom
- `id`, `organization_id`, `name`, `subject`, `grade_level`, `teacher_id`, `school_year`.

### Enrollment
- `id`, `classroom_id`, `student_id`, `joined_at`, `active`.

### Assignment
- `id`, `classroom_id`, `title`, `description`, `assignment_type`, `open_at`, `due_at`, `max_score`.

### QuestionBank
- `id`, `organization_id`, `subject`, `grade_level`, `difficulty`, `tags`, `content`, `options_json`, `answer_key`.

### ExamPaper
- `id`, `assignment_id`, `title`, `duration_minutes`, `shuffle_questions`, `shuffle_answers`.

### ExamQuestion
- `id`, `exam_paper_id`, `question_bank_id`, `order_index`, `score`.

### Submission
- `id`, `assignment_id`, `student_id`, `started_at`, `submitted_at`, `status`, `raw_answer_json`.

### SubmissionAnswer
- `id`, `submission_id`, `exam_question_id`, `answer_json`, `is_correct`, `score`.

### Grade
- `id`, `submission_id`, `grader_id`, `total_score`, `feedback`, `graded_at`.

### Notification
- `id`, `user_id`, `channel`, `title`, `content`, `is_read`, `created_at`.

### AuditLog
- `id`, `actor_id`, `action`, `target_type`, `target_id`, `meta_json`, `created_at`.

## Quan hệ chính

- User 1-N ClassRoom (teacher owner).
- ClassRoom N-N User (student) qua Enrollment.
- ClassRoom 1-N Assignment.
- Assignment 1-1 hoặc 1-N ExamPaper.
- ExamPaper 1-N ExamQuestion.
- Assignment 1-N Submission.
- Submission 1-N SubmissionAnswer.
- Submission 1-1 Grade.

## Mở rộng tương lai

- PaymentPlan, Subscription, Invoice.
- AntiCheatEvent (tab switch, device fingerprint, webcam marker).
- ParentStudentMap (phụ huynh theo dõi nhiều học sinh).
