from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from database import get_db


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.role == UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin users must be created by an existing admin")
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": create_access_token(str(user.id), user.role),
        "token_type": "bearer",
        "user": user,
    }
