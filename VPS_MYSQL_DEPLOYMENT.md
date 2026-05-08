# VPS MySQL Deployment

Your backend is already MySQL-ready. It reads the database connection from `DATABASE_URL` in `backend/.env` or from the server environment.

## 1. Create The MySQL Database

Run this on your VPS:

```sql
CREATE DATABASE ramnagari_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tour_user'@'localhost' IDENTIFIED BY 'change_this_strong_password';
GRANT ALL PRIVILEGES ON ramnagari_tourism.* TO 'tour_user'@'localhost';
FLUSH PRIVILEGES;
```

## 2. Configure Backend Environment

Create `backend/.env` on the VPS:

```env
DATABASE_URL=mysql+pymysql://tour_user:change_this_strong_password@127.0.0.1:3306/ramnagari_tourism
ALLOWED_ORIGINS=https://yourdomain.com
SECRET_KEY=change-this-to-a-long-random-secret
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_live_razorpay_secret
```

Do not put quotes around `DATABASE_URL`.

## 3. Install And Start Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

When the app starts, it creates missing tables automatically.

## 4. Seed Starting Data

Only run this if the VPS database is empty or you want the sample catalog/admin data:

```bash
cd backend
source venv/bin/activate
python seed_data.py
```

## 5. Quick Health Check

```bash
curl http://127.0.0.1:8000/api/health
```

Expected response:

```json
{"status":"ok"}
```

## 6. Production Notes

- Use a non-root MySQL user.
- Keep MySQL bound to localhost unless the database is on another server.
- Set `ALLOWED_ORIGINS` to your real website domain.
- Use Nginx as a reverse proxy from `https://yourdomain.com/api` to `http://127.0.0.1:8000`.
- Keep `backend/.env` private and never commit it.
