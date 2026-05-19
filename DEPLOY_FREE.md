# Deploy trực tuyến miễn phí (API + Web)

Tài liệu này hướng dẫn deploy bản LMS MVP lên các nền tảng miễn phí phổ biến.

## 1) Phương án khuyến nghị: Render (API + Web tĩnh)

Repo đã có sẵn `render.yaml` để one-click deploy.

### Bước làm
1. Push repo lên GitHub.
2. Vào Render -> **New +** -> **Blueprint** -> chọn repo.
3. Render đọc `render.yaml` và tạo 2 service:
   - `lms-api` (Docker web service)
   - `lms-web` (static site)
4. Tạo PostgreSQL miễn phí (Render Postgres hoặc Neon free).
5. Gán `DATABASE_URL` vào service `lms-api`.
6. Cập nhật `CORS_ORIGINS` đúng domain frontend (ví dụ `https://lms-web.onrender.com`).
7. Sửa `webapp/config.js` để trỏ `window.API_BASE` về URL API public.

## 2) Phương án 2: Railway (API) + Vercel/Netlify (Web)

### API với Railway
- Repo đã có `railway.json`.
- Tạo project Railway từ GitHub repo.
- Add PostgreSQL plugin miễn phí.
- Set env:
  - `APP_ENV=prod`
  - `APP_NAME=LMS MVP API`
  - `DATABASE_URL=<railway postgres url>`
  - `CORS_ORIGINS=<domain frontend>`

### Web với Vercel/Netlify
- Deploy thư mục `webapp/` dạng static.
- Chỉnh `webapp/config.js` để `window.API_BASE` trỏ tới URL Railway API.

## 3) Checklist trước khi public cho HS/GV

- Kiểm tra `/health` trả `status=ok`.
- Kiểm tra CORS chỉ cho phép domain thật của frontend.
- Tắt endpoint demo (`/api/seed`, `/api/reset`) nếu dùng production thật.
- Đặt mật khẩu DB mạnh và bật backup định kỳ.

## 4) Lưu ý gói miễn phí

- Có thể bị sleep khi không truy cập trong một khoảng thời gian.
- Cold start lần đầu có thể chậm 10-60 giây.
- Giới hạn CPU/RAM/băng thông tùy nền tảng.
