# Quick Start

This repo uses a root-level static frontend and a FastAPI backend in `backend/`.

## 1. Create Database

```sql
CREATE DATABASE ramnagari_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Configure Environment

Create `.env` in the project root:

```env
DATABASE_URL=mysql+pymysql://tour_user:strong_password@127.0.0.1:3306/ramnagari_tourism
ALLOWED_ORIGINS=*
```

Optional payment variables:

```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

## 3. Install Backend

```powershell
cd c:\Users\Dell\Desktop\tour\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Start Backend

```powershell
python main.py
```

Check:

```text
http://localhost:8000/api/health
```

## 5. Start Frontend

Open a new terminal:

```powershell
cd c:\Users\Dell\Desktop\tour
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

## Test Flow

1. Open `pages/booking.html`.
2. Sign up or log in.
3. Select destination, hotel category, cab type, tourists, and stay days.
4. Generate an estimate.
5. Create a booking and test the advance payment flow if Razorpay keys are configured.
6. Open `pages/admin.html` with an admin account to manage catalog and bookings.

## Admin Account

After creating a user, promote it in MySQL:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your_email@example.com';
```

## Important Paths

- Frontend home: `index.html`
- Frontend pages: `pages/`
- Styles: `css/style.css`
- Public scripts: `js/`
- Backend app: `backend/`
- API entry: `backend/main.py`
- Database config: `backend/database.py`
