# Deploy trực tuyến miễn phí (API + Web)

Tài liệu này hướng dẫn deploy bản LMS MVP lên các nền tảng miễn phí phổ biến.

## 1) Phương án A: Render (API + Web tĩnh)

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

---

## 2) Phương án B (khuyến nghị theo yêu cầu): Railway (API) + Vercel/Netlify (Web)

## 2.1 Deploy API với Railway

Repo đã có `railway.json` sẵn start command và healthcheck.

### Bước làm chi tiết
1. Push code lên GitHub.
2. Vào Railway -> **New Project** -> **Deploy from GitHub repo**.
3. Add PostgreSQL plugin trong project Railway.
4. Vào service API -> Variables, set:
   - `APP_ENV=prod`
   - `APP_NAME=LMS MVP API`
   - `DATABASE_URL=<Railway PostgreSQL URL>`
   - `CORS_ORIGINS=<domain frontend>`
5. Mở tab Deployments, đợi build xong.
6. Lấy public URL của API và test `GET /health`.

## 2.2 Deploy frontend với Vercel

1. Vào Vercel -> Import GitHub repo.
2. Chọn root directory là `webapp`.
3. Build command: để trống (static site).
4. Output directory: `.`
5. Trước khi deploy, sửa `webapp/config.js`:

```js
window.API_BASE = 'https://<your-railway-api>.up.railway.app';
```

6. Deploy và lấy URL frontend dạng `https://<project>.vercel.app`.
7. Quay lại Railway, cập nhật `CORS_ORIGINS=https://<project>.vercel.app`.

## 2.3 Deploy frontend với Netlify (nếu không dùng Vercel)

1. New site from Git -> chọn repo.
2. Base directory: `webapp`
3. Build command: để trống
4. Publish directory: `webapp`
5. Sửa `webapp/config.js` trỏ API Railway public URL.
6. Deploy và cập nhật lại `CORS_ORIGINS` trong Railway theo domain Netlify.

## 3) Checklist trước khi public cho HS/GV

- Kiểm tra `/health` trả `status=ok` và `env=prod`.
- Kiểm tra CORS chỉ cho phép domain thật của frontend.
- Tắt endpoint demo (`/api/seed`, `/api/reset`) nếu dùng production thật.
- Đặt mật khẩu DB mạnh và bật backup định kỳ.
- Kiểm tra cold start ở gói miễn phí trước giờ học/thi.

## 4) Lưu ý gói miễn phí

- Có thể bị sleep khi không truy cập trong một khoảng thời gian.
- Cold start lần đầu có thể chậm 10-60 giây.
- Giới hạn CPU/RAM/băng thông tùy nền tảng.
