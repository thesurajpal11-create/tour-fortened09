from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    PAYMENT_PENDING = "payment_pending"
    CONFIRMED = "confirmed"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class BookingPaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    ADVANCE_PAID = "advance_paid"
    PAID = "paid"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_code = Column(String(40), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    hotel_room_rate_id = Column(Integer, ForeignKey("hotel_room_rates.id"), nullable=False)
    cab_rate_id = Column(Integer, ForeignKey("cab_rates.id"), nullable=False)
    tourists = Column(Integer, nullable=False)
    stay_days = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    distance_km = Column(Float, nullable=False)
    cab_total = Column(Float, nullable=False)
    hotel_total = Column(Float, nullable=False)
    service_charge = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    advance_amount = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PAYMENT_PENDING, nullable=False)
    payment_status = Column(Enum(BookingPaymentStatus), default=BookingPaymentStatus.UNPAID, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
    destination = relationship("Destination")
    route = relationship("Route")
    hotel_room_rate = relationship("HotelRoomRate")
    cab_rate = relationship("CabRate")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    razorpay_order_id = Column(String(100), unique=True, index=True, nullable=False)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR", nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    booking = relationship("Booking")
