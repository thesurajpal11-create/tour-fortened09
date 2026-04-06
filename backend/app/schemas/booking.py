from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    destination_id: int
    service_type: str
    service_details: Optional[str] = None
    check_in_date: datetime
    check_out_date: datetime
    number_of_people: int = 1
    total_price: float

class BookingResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int
    service_type: str
    check_in_date: datetime
    check_out_date: datetime
    number_of_people: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
