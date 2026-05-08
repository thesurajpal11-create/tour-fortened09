from datetime import datetime
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_customer
from app.models.booking import Booking, BookingPaymentStatus, BookingStatus, Payment, PaymentStatus
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    PaymentOrderResponse,
    PaymentResponse,
    PaymentVerifyRequest,
)
from app.services.payments import RAZORPAY_KEY_ID, create_razorpay_order, verify_razorpay_signature
from app.services.pricing import calculate_estimate, get_rate_selection
from app.utils import hotel_option_number, public_hotel_display_name
from database import get_db


router = APIRouter(prefix="/api/bookings", tags=["Customer Bookings"])


def booking_to_response(db: Session, booking: Booking) -> BookingResponse:
    return BookingResponse(
        id=booking.id,
        booking_code=booking.booking_code,
        user_id=booking.user_id,
        destination_id=booking.destination_id,
        tour=booking.destination.name,
        hotel=booking.hotel_room_rate.category,
        hotel_option_id=booking.hotel_room_rate_id,
        display_name=public_hotel_display_name(
            booking.hotel_room_rate.category.value,
            hotel_option_number(db, booking.hotel_room_rate),
        ),
        cab=booking.cab_rate.cab_type,
        days=booking.stay_days,
        tourists=booking.tourists,
        rooms=booking.rooms,
        distance_km=booking.distance_km,
        cab_total=booking.cab_total,
        hotel_total=booking.hotel_total,
        service_charge=booking.service_charge,
        total_amount=booking.total_price,
        advance_payment_amount=booking.advance_amount,
        status=booking.status,
        payment_status=booking.payment_status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


@router.post("/", response_model=BookingResponse)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer),
):
    estimate = calculate_estimate(db, payload)
    _destination, route, cab_rate, room_rate = get_rate_selection(db, payload)
    booking = Booking(
        booking_code=f"RNT-{datetime.utcnow().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}",
        user_id=current_user.id,
        destination_id=payload.destination_id,
        route_id=route.id,
        hotel_room_rate_id=room_rate.id,
        cab_rate_id=cab_rate.id,
        tourists=payload.tourists,
        stay_days=payload.stay_days,
        rooms=estimate.rooms,
        distance_km=estimate.distance_km,
        cab_total=estimate.cab_total,
        hotel_total=estimate.hotel_total,
        service_charge=estimate.service_charge,
        total_price=estimate.total_amount,
        advance_amount=estimate.advance_payment_amount,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking_to_response(db, booking)


@router.get("/", response_model=list[BookingResponse])
def my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_customer)):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return [booking_to_response(db, booking) for booking in bookings]


@router.post("/{booking_id}/payment/order", response_model=PaymentOrderResponse)
def create_payment_order(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer),
):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    order = create_razorpay_order(booking.advance_amount, booking.booking_code)
    payment = Payment(
        booking_id=booking.id,
        razorpay_order_id=order["id"],
        amount=booking.advance_amount,
        currency=order.get("currency", "INR"),
    )
    db.add(payment)
    db.commit()
    return {
        "booking_id": booking.id,
        "razorpay_order_id": payment.razorpay_order_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "key_id": RAZORPAY_KEY_ID,
    }


@router.post("/payment/verify", response_model=PaymentResponse)
def verify_payment(
    payload: PaymentVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer),
):
    payment = db.query(Payment).filter(Payment.razorpay_order_id == payload.razorpay_order_id).first()
    if not payment or payment.booking.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Payment not found")
    if not verify_razorpay_signature(
        payload.razorpay_order_id,
        payload.razorpay_payment_id,
        payload.razorpay_signature,
    ):
        payment.status = PaymentStatus.FAILED
        db.commit()
        raise HTTPException(status_code=400, detail="Payment verification failed")

    payment.razorpay_payment_id = payload.razorpay_payment_id
    payment.razorpay_signature = payload.razorpay_signature
    payment.status = PaymentStatus.PAID
    payment.booking.payment_status = BookingPaymentStatus.ADVANCE_PAID
    payment.booking.status = BookingStatus.PENDING
    db.commit()
    db.refresh(payment)
    return payment
