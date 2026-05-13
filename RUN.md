# Run The Website

## Fast Windows Start

Open two PowerShell windows from `c:\Users\Dell\Desktop\tour`.

### Window 1: Backend

```powershell
.\start-backend.bat
```

The API should start at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### Window 2: Frontend

```powershell
.\start-frontend.bat
```

The website should start at:

```text
http://localhost:5500
```

## Manual Commands

### Backend

```powershell
cd c:\Users\Dell\Desktop\tour\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend

```powershell
cd c:\Users\Dell\Desktop\tour
python -m http.server 5500
```

## Pages To Test

| Page | URL |
| --- | --- |
| Home | `http://localhost:5500` |
| Destinations | `http://localhost:5500/pages/destinations.html` |
| Tour Packages | `http://localhost:5500/pages/tour-packages.html` |
| Hotels | `http://localhost:5500/pages/hotels.html` |
| Booking | `http://localhost:5500/pages/booking.html` |
| Cab Tariff | `http://localhost:5500/pages/cab.html` |
| Contact | `http://localhost:5500/pages/contact.html` |
| Admin | `http://localhost:5500/pages/admin.html` |

## Database Notes

Create a MySQL database first:

```sql
CREATE DATABASE ramnagari_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Set the root `.env` file:

```env
DATABASE_URL=mysql+pymysql://tour_user:strong_password@127.0.0.1:3306/ramnagari_tourism
ALLOWED_ORIGINS=*
```

Tables are created or checked when the backend starts.

## Troubleshooting

- If port `5500` is busy, run `python -m http.server 5501` and open `http://localhost:5501`.
- If port `8000` is busy, stop the old backend process or change the port in `backend/main.py`.
- If the website cannot load catalog data, confirm `http://localhost:8000/api/health` returns `{"status":"ok"}`.
- If MySQL fails, check that `DATABASE_URL` points to the correct user, password, host, and database.
