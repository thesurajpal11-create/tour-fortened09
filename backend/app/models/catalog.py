from datetime import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class HotelCategory(str, enum.Enum):
    BUDGET = "Budget"
    TWO_STAR = "2 Star"
    THREE_STAR = "3 Star"
    FOUR_STAR = "4 Star"


class CabType(str, enum.Enum):
    SEDAN = "Sedan"
    SUV = "SUV"
    INNOVA = "Innova"
    TEMPO_TRAVELLER = "Tempo Traveller"


class Route(Base):
    __tablename__ = "routes"
    __table_args__ = (UniqueConstraint("origin", "destination_id", name="uq_route_origin_destination"),)

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(100), default="Ayodhya", nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    distance_km = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    destination = relationship("Destination")


class CabRate(Base):
    __tablename__ = "cab_rates"

    id = Column(Integer, primary_key=True, index=True)
    cab_type = Column(Enum(CabType), unique=True, nullable=False)
    rate_per_km = Column(Float, nullable=False)
    driver_allowance_per_day = Column(Float, default=0.0, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HotelOwner(Base):
    __tablename__ = "hotel_owners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")


class HiddenHotel(Base):
    __tablename__ = "hidden_hotels"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("hotel_owners.id"), nullable=False)
    real_hotel_name = Column(String(160), nullable=False)
    address = Column(String(255), nullable=True)
    nearby_place = Column(String(160), nullable=True)
    distance_from_destination_km = Column(Float, default=0.0, nullable=False)
    amenities = Column(Text, nullable=True)
    check_in_time = Column(String(20), default="12:00 PM", nullable=False)
    check_out_time = Column(String(20), default="11:00 AM", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    destination = relationship("Destination")
    owner = relationship("HotelOwner")
    room_rates = relationship("HotelRoomRate", back_populates="hotel")


class HotelRoomRate(Base):
    __tablename__ = "hotel_room_rates"
    __table_args__ = (UniqueConstraint("hotel_id", "category", name="uq_hotel_category"),)

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hidden_hotels.id"), nullable=False)
    category = Column(Enum(HotelCategory), nullable=False)
    base_price_per_room = Column(Float, nullable=False)
    selling_price_per_room = Column(Float, nullable=False)
    rooms_available = Column(Integer, default=10, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hotel = relationship("HiddenHotel", back_populates="room_rates")

    @property
    def margin(self) -> float:
        return self.selling_price_per_room - self.base_price_per_room
