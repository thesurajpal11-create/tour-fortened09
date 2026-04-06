from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from database import Base

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=4.5)
    reviews_count = Column(Integer, default=0)
    best_time_to_visit = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
