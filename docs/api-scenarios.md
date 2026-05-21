# API scenarios & implementation kịch bản

## 1) Auth & RBAC

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/me`

Kịch bản:
1. User đăng nhập nhận access token + refresh token.
2. Middleware kiểm tra JWT, inject `current_user`.
3. Policy kiểm tra role/ownership theo endpoint.

## 2) Class management

- `POST /api/v1/classes`
- `GET /api/v1/classes`
- `GET /api/v1/classes/{class_id}`
- `POST /api/v1/classes/{class_id}/enrollments`
- `DELETE /api/v1/classes/{class_id}/enrollments/{student_id}`

Kịch bản:
1. Teacher tạo lớp.
2. Import danh sách học sinh.
3. Student join bằng class code (tuỳ chọn).

## 3) Assignment & exam

- `POST /api/v1/classes/{class_id}/assignments`
- `GET /api/v1/assignments/{assignment_id}`
- `POST /api/v1/assignments/{assignment_id}/exam-paper`
- `POST /api/v1/assignments/{assignment_id}/publish`

Kịch bản:
1. Teacher chọn câu hỏi từ question bank.
2. Hệ thống sinh exam paper.
3. Teacher publish theo `open_at/due_at`.

## 4) Student submission

- `POST /api/v1/assignments/{assignment_id}/submissions/start`
- `PUT /api/v1/submissions/{submission_id}/answers`
- `POST /api/v1/submissions/{submission_id}/submit`

Kịch bản:
1. Student bắt đầu bài => lock timer.
2. Auto-save đáp án mỗi 10-20 giây.
3. Submit hoặc auto-submit khi hết giờ.

## 5) Grading & analytics

- `POST /api/v1/submissions/{submission_id}/grade`
- `GET /api/v1/classes/{class_id}/gradebook`
- `GET /api/v1/students/{student_id}/progress`

Kịch bản:
1. Chấm tự động câu trắc nghiệm.
2. Chấm tay câu tự luận.
3. Tổng hợp điểm và biểu đồ tiến độ.

## 6) Notification flow

- `POST /api/v1/notifications/broadcast`
- `GET /api/v1/notifications`
- `POST /api/v1/notifications/{id}/read`

Kịch bản:
- Khi publish assignment => push notification cho toàn lớp.
