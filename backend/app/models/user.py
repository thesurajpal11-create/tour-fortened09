from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from database import Base
import enum


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    HOTEL_OWNER = "hotel_owner"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
