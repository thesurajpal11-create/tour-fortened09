from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DestinationCreate(BaseModel):
    name: str
    description: str
    short_description: str
    image_url: Optional[str] = None
    best_time_to_visit: Optional[str] = None

class DestinationUpdate(BaseModel):
    description: Optional[str] = None
    short_description: Optional[str] = None
    image_url: Optional[str] = None
    best_time_to_visit: Optional[str] = None

class DestinationResponse(BaseModel):
    id: int
    name: str
    description: str
    short_description: str
    image_url: Optional[str]
    rating: float
    reviews_count: int
    best_time_to_visit: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
