from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.booking import BookingPaymentStatus, BookingStatus, PaymentStatus
from app.models.catalog import CabType, HotelCategory


class EstimateRequest(BaseModel):
    destination_id: int
    hotel_category: HotelCategory
    cab_type: CabType
    tourists: int = Field(..., ge=1)
    stay_days: int = Field(..., ge=1)
    hotel_option_id: Optional[int] = None


class EstimateResponse(BaseModel):
    destination_id: int
    tour: str
    hotel: HotelCategory
    hotel_option_id: Optional[int] = None
    display_name: str
    cab: CabType
    days: int
    tourists: int
    rooms: int
    distance_km: float
    cab_total: float
    hotel_total: float
    service_charge: float
    total_amount: float
    advance_payment_amount: float
    currency: str = "INR"


class BookingCreate(EstimateRequest):
    pass


class BookingResponse(EstimateResponse):
    id: int
    booking_code: str
    user_id: int
    status: BookingStatus
    payment_status: BookingPaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminBookingResponse(BookingResponse):
    customer_name: str
    customer_email: str
    real_hotel_name: str
    owner_name: str
    base_price_per_room: float
    selling_price_per_room: float
    margin: float


class BookingStatusUpdate(BaseModel):
    status: BookingStatus


class PaymentOrderResponse(BaseModel):
    booking_id: int
    razorpay_order_id: str
    amount: float
    currency: str = "INR"
    key_id: str


class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    invoice_number: str
    booking_code: str
    customer_name: str
    tour: str
    hotel_category: HotelCategory
    cab_type: CabType
    tourists: int
    stay_days: int
    rooms: int
    total_amount: float
    advance_paid: float
    balance_amount: float
    status: BookingStatus
    generated_at: datetime
