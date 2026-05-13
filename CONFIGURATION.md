# Configuration

## Database

The backend reads `DATABASE_URL` from environment variables. Keep the value in the project root `.env` file for local Windows runs.

```env
DATABASE_URL=mysql+pymysql://tour_user:strong_password@127.0.0.1:3306/ramnagari_tourism
```

Create the database before starting the backend:

```sql
CREATE DATABASE ramnagari_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## CORS

For local development:

```env
ALLOWED_ORIGINS=*
```

For production, use the public website origin:

```env
ALLOWED_ORIGINS=https://www.ramnagritourism.com
```

## Payments

Razorpay is optional for local browsing, but required for the live advance payment flow.

```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

## API URL Used By Frontend

Booking scripts default to:

```javascript
http://127.0.0.1:8000
```

To override before loading `js/booking.js`, define:

```html
<script>
  window.RAMNAGARI_API_BASE_URL = "https://api.example.com";
</script>
```

## Branding And Contact Details

Common files:

- `index.html`
- `pages/contact.html`
- `pages/booking.html`
- `css/style.css`

Search for:

- `7607745628`
- `Ayodhya Ramnagri Tourism`
- `ramnagritourism.com`

## Catalog And Pricing

Public catalog data is served through:

- `GET /api/catalog/destinations`
- `GET /api/catalog/tour-packages`
- `GET /api/catalog/hotel-types`
- `GET /api/catalog/hotel-options`
- `GET /api/catalog/cab-types`

Admin catalog management is served through:

- `/api/admin/destinations`
- `/api/admin/routes`
- `/api/admin/cab-rates`
- `/api/admin/hotel-owners`
- `/api/admin/hidden-hotels`
- `/api/admin/hotel-room-rates`

## Local Scripts

- `start-backend.bat`: starts the FastAPI backend from `backend/`.
- `start-frontend.bat`: serves the repository root with Python HTTP server.
- `verify-deployment.bat`: checks important local files before deployment.
