# Ayodhya Ramnagri Tourism

Tour and travel website for Ayodhya Ramnagri Tourism, with a static frontend and a FastAPI backend for catalog, booking, payment, and admin workflows.

## What Is Included

- Public website pages for destinations, tour packages, hotels, cab tariff, booking, and contact.
- Customer signup/login, trip estimate, booking, and advance payment flow.
- Admin panel for destinations, routes, cab rates, hotel owners, hidden hotel rates, and bookings.
- MySQL-backed FastAPI API with SQLAlchemy models and automatic schema checks.
- SEO files including `robots.txt`, `sitemap.xml`, social preview image, and Google verification files.

## Project Layout

```text
tour/
|-- index.html
|-- pages/
|   |-- destinations.html
|   |-- tour-packages.html
|   |-- hotels.html
|   |-- booking.html
|   |-- cab.html
|   |-- contact.html
|   `-- admin.html
|-- destinations/
|-- css/
|-- js/
|-- images/
|-- backend/
|   |-- main.py
|   |-- database.py
|   |-- requirements.txt
|   `-- app/
|-- start-backend.bat
|-- start-frontend.bat
`-- verify-deployment.bat
```

There is no separate `frontend/` folder. Serve the repository root to run the website.

## Requirements

- Python 3.8+
- MySQL server
- A browser

## Setup

1. Create a MySQL database:

   ```sql
   CREATE DATABASE ramnagari_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Create or update `.env` in the project root:

   ```env
   DATABASE_URL=mysql+pymysql://tour_user:strong_password@127.0.0.1:3306/ramnagari_tourism
   ALLOWED_ORIGINS=*
   ```

3. Install backend dependencies:

   ```powershell
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Start the backend:

   ```powershell
   python main.py
   ```

5. In a second terminal, serve the frontend from the project root:

   ```powershell
   cd c:\Users\Dell\Desktop\tour
   python -m http.server 5500
   ```

6. Open:

   ```text
   http://localhost:5500
   ```

## Useful URLs

| Area | URL |
| --- | --- |
| Website | `http://localhost:5500` |
| Booking page | `http://localhost:5500/pages/booking.html` |
| Admin panel | `http://localhost:5500/pages/admin.html` |
| API health | `http://localhost:8000/api/health` |
| API docs | `http://localhost:8000/docs` |

## API Summary

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/catalog/destinations`
- `GET /api/catalog/tour-packages`
- `GET /api/catalog/hotel-types`
- `GET /api/catalog/hotel-options`
- `GET /api/catalog/cab-types`
- `POST /api/catalog/estimate`
- `POST /api/bookings/`
- `GET /api/bookings/`
- `POST /api/bookings/{booking_id}/payment/order`
- `POST /api/bookings/payment/verify`
- `GET /api/admin/bookings`
- `PUT /api/admin/bookings/{booking_id}/approve`
- `PUT /api/admin/bookings/{booking_id}/cancel`

## Quick Scripts

- `start-backend.bat` checks Python, creates the backend venv if needed, installs dependencies, and starts FastAPI.
- `start-frontend.bat` serves the repository root at `http://localhost:5500`.
- `verify-deployment.bat` checks the expected project files before deployment.

## Support Details

- Phone/WhatsApp: `7607745628`
- Domain: `https://www.ramnagritourism.com/`
