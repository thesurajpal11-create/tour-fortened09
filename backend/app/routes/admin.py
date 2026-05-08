from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_admin
from app.auth.security import hash_password
from app.models.booking import Booking, BookingStatus
from app.models.catalog import CabRate, HiddenHotel, HotelOwner, HotelRoomRate, Route
from app.models.destination import Destination
from app.models.user import User, UserRole
from app.schemas.booking import AdminBookingResponse, BookingStatusUpdate, InvoiceResponse
from app.schemas.catalog import (
    CabRateCreate,
    CabRateResponse,
    CabRateUpdate,
    HiddenHotelCreate,
    HiddenHotelResponse,
    HiddenHotelUpdate,
    HotelOwnerCreate,
    HotelOwnerResponse,
    HotelOwnerUpdate,
    HotelRoomRateCreate,
    HotelRoomRateResponse,
    HotelRoomRateUpdate,
    RouteCreate,
    RouteResponse,
    RouteUpdate,
)
from app.schemas.destination import DestinationCreate, DestinationResponse, DestinationUpdate
from app.schemas.user import UserCreate, UserResponse
from app.routes.bookings import booking_to_response
from app.utils import apply_updates, encode_amenities, hidden_hotel_response
from database import get_db


router = APIRouter(prefix="/api/admin", tags=["Admin Panel"], dependencies=[Depends(get_current_admin)])


def get_or_404(db: Session, model, object_id: int):
    instance = db.query(model).filter(model.id == object_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return instance


def save(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def room_rate_response(rate: HotelRoomRate) -> HotelRoomRateResponse:
    return HotelRoomRateResponse(
        id=rate.id,
        hotel_id=rate.hotel_id,
        category=rate.category,
        base_price_per_room=rate.base_price_per_room,
        selling_price_per_room=rate.selling_price_per_room,
        rooms_available=rate.rooms_available,
        is_active=rate.is_active,
        real_hotel_name=rate.hotel.real_hotel_name if rate.hotel else None,
        owner_name=rate.hotel.owner.owner_name if rate.hotel and rate.hotel.owner else None,
        margin=rate.margin,
        created_at=rate.created_at,
        updated_at=rate.updated_at,
    )

def admin_booking_response(db: Session, booking: Booking) -> AdminBookingResponse:
    public = booking_to_response(db, booking).model_dump()
    room_rate = booking.hotel_room_rate
    hotel = room_rate.hotel
    return AdminBookingResponse(
        **public,
        customer_name=booking.user.name,
        customer_email=booking.user.email,
        real_hotel_name=hotel.real_hotel_name,
        owner_name=hotel.owner.owner_name,
        base_price_per_room=room_rate.base_price_per_room,
        selling_price_per_room=room_rate.selling_price_per_room,
        margin=room_rate.margin,
    )


@router.post("/users/admin", response_model=UserResponse)
def create_admin_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        role=UserRole.ADMIN,
        hashed_password=hash_password(payload.password),
    )
    return save(db, user)


@router.get("/destinations", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    return db.query(Destination).all()


@router.post("/destinations", response_model=DestinationResponse)
def create_destination(payload: DestinationCreate, db: Session = Depends(get_db)):
    return save(db, Destination(**payload.model_dump()))


@router.put("/destinations/{destination_id}", response_model=DestinationResponse)
def update_destination(destination_id: int, payload: DestinationUpdate, db: Session = Depends(get_db)):
    destination = get_or_404(db, Destination, destination_id)
    apply_updates(destination, payload.model_dump(exclude_unset=True))
    return save(db, destination)


@router.delete("/destinations/{destination_id}", response_model=DestinationResponse)
def disable_destination(destination_id: int, db: Session = Depends(get_db)):
    destination = get_or_404(db, Destination, destination_id)
    destination.is_active = False
    return save(db, destination)


@router.get("/routes", response_model=list[RouteResponse])
def list_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()


@router.post("/routes", response_model=RouteResponse)
def create_route(payload: RouteCreate, db: Session = Depends(get_db)):
    return save(db, Route(**payload.model_dump()))


@router.put("/routes/{route_id}", response_model=RouteResponse)
def update_route(route_id: int, payload: RouteUpdate, db: Session = Depends(get_db)):
    route = get_or_404(db, Route, route_id)
    apply_updates(route, payload.model_dump(exclude_unset=True))
    return save(db, route)


@router.get("/cab-rates", response_model=list[CabRateResponse])
def list_cab_rates(db: Session = Depends(get_db)):
    return db.query(CabRate).all()


@router.post("/cab-rates", response_model=CabRateResponse)
def create_cab_rate(payload: CabRateCreate, db: Session = Depends(get_db)):
    return save(db, CabRate(**payload.model_dump()))


@router.put("/cab-rates/{cab_rate_id}", response_model=CabRateResponse)
def update_cab_rate(cab_rate_id: int, payload: CabRateUpdate, db: Session = Depends(get_db)):
    cab_rate = get_or_404(db, CabRate, cab_rate_id)
    apply_updates(cab_rate, payload.model_dump(exclude_unset=True))
    return save(db, cab_rate)


@router.get("/hotel-owners", response_model=list[HotelOwnerResponse])
def list_hotel_owners(db: Session = Depends(get_db)):
    return db.query(HotelOwner).all()


@router.post("/hotel-owners", response_model=HotelOwnerResponse)
def create_hotel_owner(payload: HotelOwnerCreate, db: Session = Depends(get_db)):
    return save(db, HotelOwner(**payload.model_dump()))


@router.put("/hotel-owners/{owner_id}", response_model=HotelOwnerResponse)
def update_hotel_owner(owner_id: int, payload: HotelOwnerUpdate, db: Session = Depends(get_db)):
    owner = get_or_404(db, HotelOwner, owner_id)
    apply_updates(owner, payload.model_dump(exclude_unset=True))
    return save(db, owner)


@router.get("/hidden-hotels", response_model=list[HiddenHotelResponse])
def list_hidden_hotels(db: Session = Depends(get_db)):
    return [hidden_hotel_response(hotel) for hotel in db.query(HiddenHotel).all()]


@router.post("/hidden-hotels", response_model=HiddenHotelResponse)
def create_hidden_hotel(payload: HiddenHotelCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["amenities"] = encode_amenities(data.get("amenities"))
    hotel = save(db, HiddenHotel(**data))
    return hidden_hotel_response(hotel)


@router.put("/hidden-hotels/{hotel_id}", response_model=HiddenHotelResponse)
def update_hidden_hotel(hotel_id: int, payload: HiddenHotelUpdate, db: Session = Depends(get_db)):
    hotel = get_or_404(db, HiddenHotel, hotel_id)
    data = payload.model_dump(exclude_unset=True)
    if "amenities" in data:
        data["amenities"] = encode_amenities(data["amenities"])
    apply_updates(hotel, data)
    return hidden_hotel_response(save(db, hotel))


@router.get("/hotel-room-rates", response_model=list[HotelRoomRateResponse])
def list_hotel_room_rates(db: Session = Depends(get_db)):
    return [room_rate_response(rate) for rate in db.query(HotelRoomRate).all()]


@router.post("/hotel-room-rates", response_model=HotelRoomRateResponse)
def create_hotel_room_rate(payload: HotelRoomRateCreate, db: Session = Depends(get_db)):
    rate = save(db, HotelRoomRate(**payload.model_dump()))
    return room_rate_response(rate)


@router.put("/hotel-room-rates/{rate_id}", response_model=HotelRoomRateResponse)
def update_hotel_room_rate(rate_id: int, payload: HotelRoomRateUpdate, db: Session = Depends(get_db)):
    rate = get_or_404(db, HotelRoomRate, rate_id)
    apply_updates(rate, payload.model_dump(exclude_unset=True))
    return room_rate_response(save(db, rate))


@router.get("/bookings", response_model=list[AdminBookingResponse])
def view_bookings(db: Session = Depends(get_db)):
    return [admin_booking_response(db, booking) for booking in db.query(Booking).all()]


@router.put("/bookings/{booking_id}/status", response_model=AdminBookingResponse)
def update_booking_status(booking_id: int, payload: BookingStatusUpdate, db: Session = Depends(get_db)):
    booking = get_or_404(db, Booking, booking_id)
    booking.status = payload.status
    return admin_booking_response(db, save(db, booking))


@router.put("/bookings/{booking_id}/approve", response_model=AdminBookingResponse)
def approve_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_or_404(db, Booking, booking_id)
    booking.status = BookingStatus.APPROVED
    return admin_booking_response(db, save(db, booking))


@router.put("/bookings/{booking_id}/cancel", response_model=AdminBookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_or_404(db, Booking, booking_id)
    booking.status = BookingStatus.CANCELLED
    return admin_booking_response(db, save(db, booking))


@router.get("/bookings/{booking_id}/invoice", response_model=InvoiceResponse)
def generate_invoice(booking_id: int, db: Session = Depends(get_db)):
    booking = get_or_404(db, Booking, booking_id)
    advance_paid = booking.advance_amount if booking.payment_status.value != "unpaid" else 0.0
    return InvoiceResponse(
        invoice_number=f"INV-{booking.booking_code}",
        booking_code=booking.booking_code,
        customer_name=booking.user.name,
        tour=booking.destination.name,
        hotel_category=booking.hotel_room_rate.category,
        cab_type=booking.cab_rate.cab_type,
        tourists=booking.tourists,
        stay_days=booking.stay_days,
        rooms=booking.rooms,
        total_amount=booking.total_price,
        advance_paid=advance_paid,
        balance_amount=round(booking.total_price - advance_paid, 2),
        status=booking.status,
        generated_at=datetime.utcnow(),
    )
