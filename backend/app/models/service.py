from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    service_type = Column(String(100), nullable=False)  # hotel, tour, transportation, package, restaurant
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String(50), default="per night")  # per night, per hour, per day, per person, etc
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=4.5)
    contact_info = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
