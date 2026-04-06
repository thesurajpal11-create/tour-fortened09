from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceCreate(BaseModel):
    destination_id: int
    service_type: str  # hotel, tour, transportation, package, restaurant
    name: str
    description: str
    price_per_unit: float
    unit: str = "per night"
    image_url: Optional[str] = None
    contact_info: Optional[str] = None

class ServiceResponse(BaseModel):
    id: int
    destination_id: int
    service_type: str
    name: str
    description: str
    price_per_unit: float
    unit: str
    image_url: Optional[str]
    rating: float
    contact_info: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
