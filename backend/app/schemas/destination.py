from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DestinationBase(BaseModel):
    name: str
    description: str
    short_description: str
    image_url: Optional[str] = None
    base_package_price: float = 0.0
    best_time_to_visit: Optional[str] = None
    is_active: bool = True


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    image_url: Optional[str] = None
    base_package_price: Optional[float] = None
    best_time_to_visit: Optional[str] = None
    is_active: Optional[bool] = None


class DestinationResponse(DestinationBase):
    id: int
    rating: float
    reviews_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
