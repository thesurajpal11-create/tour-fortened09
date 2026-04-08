import os
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from app.models.user import User
from app.models.destination import Destination
from app.models.booking import Booking
from app.models.service import Service
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.destination import DestinationCreate, DestinationResponse
from app.schemas.booking import BookingCreate, BookingResponse
from app.schemas.service import ServiceCreate, ServiceResponse
import secrets

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="Ayodhya Ramnagari Tourism API", version="1.0.0")

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins.strip() == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Token storage (In production, use JWT)
tokens_store = {}

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_token() -> str:
    return secrets.token_urlsafe(32)

# ==================== AUTH ROUTES ====================
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@auth_router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        phone=user.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}

@auth_router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return token"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    token = generate_token()
    tokens_store[token] = {"user_id": user.id, "email": user.email}
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }

# ==================== DESTINATION ROUTES ====================
destination_router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@destination_router.get("/")
def get_destinations(db: Session = Depends(get_db)):
    """Get all destinations"""
    destinations = db.query(Destination).all()
    return destinations

@destination_router.get("/{destination_id}")
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Get specific destination"""
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@destination_router.post("/")
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    """Create new destination (Admin only)"""
    new_destination = Destination(
        name=destination.name,
        description=destination.description,
        short_description=destination.short_description,
        image_url=destination.image_url,
        best_time_to_visit=destination.best_time_to_visit
    )
    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)
    return new_destination

# ==================== BOOKING ROUTES ====================
booking_router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authorization token"""
    token = credentials.credentials
    if token not in tokens_store:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens_store[token]

@booking_router.post("/")
def create_booking(booking: BookingCreate, user_info = Depends(verify_token), db: Session = Depends(get_db)):
    """Create a new booking"""
    user_id = user_info["user_id"]
    
    new_booking = Booking(
        user_id=user_id,
        destination_id=booking.destination_id,
        service_type=booking.service_type,
        service_details=booking.service_details,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        number_of_people=booking.number_of_people,
        total_price=booking.total_price
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@booking_router.get("/")
def get_user_bookings(user_info = Depends(verify_token), db: Session = Depends(get_db)):
    """Get user's bookings"""
    user_id = user_info["user_id"]
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return bookings

@booking_router.get("/{booking_id}")
def get_booking(booking_id: int, user_info = Depends(verify_token), db: Session = Depends(get_db)):
    """Get specific booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user_info["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return booking

# ==================== SERVICE ROUTES ====================
service_router = APIRouter(prefix="/api/services", tags=["Services"])

@service_router.get("/destination/{destination_id}")
def get_destination_services(destination_id: int, db: Session = Depends(get_db)):
    """Get services for a destination"""
    services = db.query(Service).filter(Service.destination_id == destination_id).all()
    return services

@service_router.post("/")
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Create new service"""
    new_service = Service(
        destination_id=service.destination_id,
        service_type=service.service_type,
        name=service.name,
        description=service.description,
        price_per_unit=service.price_per_unit,
        unit=service.unit,
        image_url=service.image_url,
        contact_info=service.contact_info
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# ==================== ADMIN ROUTES ====================
admin_router = APIRouter(prefix="/api/admin", tags=["Admin"])

@admin_router.get("/bookings")
def get_all_bookings(user_info = Depends(verify_token), db: Session = Depends(get_db)):
    """Get all bookings (Admin only)"""
    user = db.query(User).filter(User.id == user_info["user_id"]).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    bookings = db.query(Booking).all()
    return bookings

@admin_router.put("/bookings/{booking_id}/status")
def update_booking_status(booking_id: int, status: str, user_info = Depends(verify_token), db: Session = Depends(get_db)):
    """Update booking status (Admin only)"""
    user = db.query(User).filter(User.id == user_info["user_id"]).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = status
    booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking

# Include routers
app.include_router(auth_router)
app.include_router(destination_router)
app.include_router(booking_router)
app.include_router(service_router)
app.include_router(admin_router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Ayodhya Ramnagari Tourism API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "destinations": "/api/destinations",
            "bookings": "/api/bookings",
            "services": "/api/services",
            "admin": "/api/admin"
        }
    }

@app.get("/api/")
def api_root():
    return {
        "message": "Ayodhya Ramnagari Tourism API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
