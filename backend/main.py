from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from app.models import *  # noqa: F403
from app.db_schema import ensure_catalog_schema
from app.routes import admin, auth, bookings, destinations, media
from database import Base, engine


Base.metadata.create_all(bind=engine)
ensure_catalog_schema(engine)

app = FastAPI(
    title="Ramnagari Tourism API",
    description="FastAPI and MySQL backend for public tour browsing, authenticated booking, Razorpay advance payments, and admin management.",
    version="2.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
origins = ["*"] if allowed_origins.strip() == "*" else [
    origin.strip() for origin in allowed_origins.split(",") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(bookings.router)
app.include_router(admin.router)
app.include_router(media.router)

uploads_dir = Path(__file__).resolve().parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Welcome to Ramnagari Tourism API",
        "docs": "/docs",
        "public_catalog": "/api/catalog",
        "auth": "/api/auth",
        "bookings": "/api/bookings",
        "admin": "/api/admin",
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
