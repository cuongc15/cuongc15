# Nền tảng LMS/Thi trực tuyến (blueprint)

Tài liệu này cung cấp blueprint để xây dựng một hệ thống tương tự về **chức năng** (không sao chép dữ liệu trái phép từ website bên thứ ba).

## 1) Phạm vi MVP

- Quản lý người dùng: admin, giáo viên, học sinh, phụ huynh.
- Quản lý lớp học, môn học, ghi danh.
- Giao bài tập/đề kiểm tra, nộp bài, chấm điểm.
- Ngân hàng câu hỏi và sinh đề.
- Báo cáo tiến độ học tập theo lớp/học sinh.

## 2) Kiến trúc đề xuất

- Frontend: Web tĩnh (`webapp/`) gọi REST API.
- Backend API: FastAPI (`backend/main.py`).
- DB: PostgreSQL.
- Runtime config: `.env`/biến môi trường.

Xem chi tiết tại:
- `docs/domain-model.md`
- `docs/api-scenarios.md`
- `database/schema.sql`

## 3) Chạy local bằng Python

### 3.1 Chuẩn bị PostgreSQL

```bash
createdb lms_platform
```

### 3.2 Cài dependencies backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3.3 Chạy FastAPI

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 3.4 Chạy web UI

```bash
cd webapp
python3 -m http.server 8080
```

Mở `http://localhost:8080` để dùng giao diện. UI đọc `API_BASE` từ `webapp/config.js`.

## 4) Chạy production-ready bằng Docker Compose

```bash
docker compose up --build -d
```

- API: `http://localhost:8000/health`
- DB: PostgreSQL `localhost:5432`
- Web UI: chạy riêng bằng static hosting hoặc `python3 -m http.server 8080` trong thư mục `webapp/`.

## 5) Biến môi trường production

- `APP_ENV`: `dev`/`prod`
- `APP_NAME`: tên dịch vụ API
- `DATABASE_URL`: PostgreSQL URL
- `CORS_ORIGINS`: danh sách domain cách nhau bởi dấu phẩy (ví dụ `https://app.yourdomain.com`)

## 6) Lưu ý pháp lý/kỹ thuật crawl

Nếu thu thập dữ liệu công khai để nghiên cứu thị trường:

- Đọc và tuân thủ `robots.txt`, Terms of Service, Privacy Policy.
- Không thu thập dữ liệu cá nhân nhạy cảm khi chưa có quyền hợp pháp.
- Áp dụng rate-limit và user-agent rõ ràng.
- Ưu tiên API chính thức hoặc dữ liệu do chính tổ chức bạn sở hữu.

## 7) Deploy trực tuyến miễn phí

- Dùng Render Blueprint: `render.yaml` (API + web tĩnh).
- Hoặc Railway cho API + Vercel/Netlify cho frontend.
- Xem chi tiết tại `DEPLOY_FREE.md`.


## 8) Triển khai phương án B (Railway + Vercel/Netlify)

- API deploy trên Railway: dùng `railway.json`.
- Frontend deploy trên Vercel/Netlify: dùng thư mục `webapp/`.
- Đổi `webapp/config.js` theo mẫu `webapp/config.production.example.js`.
- Xem checklist chi tiết tại `DEPLOY_FREE.md` (mục 2).
