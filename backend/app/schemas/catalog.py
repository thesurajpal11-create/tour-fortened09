from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.catalog import CabType, HotelCategory


class RouteBase(BaseModel):
    origin: str = "Ayodhya"
    destination_id: int
    distance_km: float
    is_active: bool = True


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    origin: Optional[str] = None
    destination_id: Optional[int] = None
    distance_km: Optional[float] = None
    is_active: Optional[bool] = None


class RouteResponse(RouteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CabRateBase(BaseModel):
    cab_type: CabType
    rate_per_km: float
    driver_allowance_per_day: float = 0.0
    capacity: int
    is_active: bool = True


class CabRateCreate(CabRateBase):
    pass


class CabRateUpdate(BaseModel):
    cab_type: Optional[CabType] = None
    rate_per_km: Optional[float] = None
    driver_allowance_per_day: Optional[float] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class CabRateResponse(CabRateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HotelOwnerBase(BaseModel):
    owner_name: str
    email: EmailStr
    phone: Optional[str] = None
    user_id: Optional[int] = None
    is_active: bool = True


class HotelOwnerCreate(HotelOwnerBase):
    pass


class HotelOwnerUpdate(BaseModel):
    owner_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_id: Optional[int] = None
    is_active: Optional[bool] = None


class HotelOwnerResponse(HotelOwnerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HiddenHotelBase(BaseModel):
    destination_id: int
    owner_id: int
    real_hotel_name: str
    address: Optional[str] = None
    nearby_place: Optional[str] = None
    distance_from_destination_km: float = 0.0
    amenities: list[str] = []
    check_in_time: str = "12:00 PM"
    check_out_time: str = "11:00 AM"
    is_active: bool = True


class HiddenHotelCreate(HiddenHotelBase):
    pass


class HiddenHotelUpdate(BaseModel):
    destination_id: Optional[int] = None
    owner_id: Optional[int] = None
    real_hotel_name: Optional[str] = None
    address: Optional[str] = None
    nearby_place: Optional[str] = None
    distance_from_destination_km: Optional[float] = None
    amenities: Optional[list[str]] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    is_active: Optional[bool] = None


class HiddenHotelResponse(HiddenHotelBase):
    id: int
    owner_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HotelRoomRateBase(BaseModel):
    hotel_id: int
    category: HotelCategory
    base_price_per_room: float
    selling_price_per_room: float
    rooms_available: int = 10
    is_active: bool = True


class HotelRoomRateCreate(HotelRoomRateBase):
    pass


class HotelRoomRateUpdate(BaseModel):
    hotel_id: Optional[int] = None
    category: Optional[HotelCategory] = None
    base_price_per_room: Optional[float] = None
    selling_price_per_room: Optional[float] = None
    rooms_available: Optional[int] = None
    is_active: Optional[bool] = None


class HotelRoomRateResponse(HotelRoomRateBase):
    id: int
    real_hotel_name: Optional[str] = None
    owner_name: Optional[str] = None
    margin: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PublicHotelType(BaseModel):
    category: HotelCategory
    display_name: str


class PublicCabType(BaseModel):
    cab_type: CabType
    rate_per_km: float
    driver_allowance_per_day: float
    capacity: int

    class Config:
        from_attributes = True


class PublicTourPackage(BaseModel):
    destination_id: int
    tour: str
    short_description: str
    base_package_price: float
    best_time_to_visit: Optional[str] = None


class PublicHotelOption(BaseModel):
    hotel_option_id: int
    destination_id: int
    category: HotelCategory
    display_name: str
    selling_price_per_room: float
    rooms_available: int
    nearby_place: Optional[str] = None
    distance_from_tour_km: float
    amenities: list[str]
    check_in_time: str
    check_out_time: str
