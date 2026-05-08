# Initialization file for models
from app.models.booking import Booking, BookingStatus, Payment, PaymentStatus
from app.models.catalog import CabRate, CabType, HiddenHotel, HotelCategory, HotelOwner, HotelRoomRate, Route
from app.models.destination import Destination
from app.models.user import User, UserRole

__all__ = [
    "Booking",
    "BookingStatus",
    "CabRate",
    "CabType",
    "Destination",
    "HiddenHotel",
    "HotelCategory",
    "HotelOwner",
    "HotelRoomRate",
    "Payment",
    "PaymentStatus",
    "Route",
    "User",
    "UserRole",
]
