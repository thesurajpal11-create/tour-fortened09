from math import ceil

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.catalog import CabRate, CabType, HiddenHotel, HotelCategory, HotelRoomRate, Route
from app.models.destination import Destination
from app.schemas.booking import EstimateRequest, EstimateResponse
from app.utils import hotel_option_number, public_hotel_display_name


SERVICE_CHARGE_PERCENT = 10
ADVANCE_PERCENT = 30
TOURISTS_PER_ROOM = 2


def get_rate_selection(db: Session, payload: EstimateRequest):
    destination = (
        db.query(Destination)
        .filter(Destination.id == payload.destination_id, Destination.is_active.is_(True))
        .first()
    )
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    route = (
        db.query(Route)
        .filter(Route.destination_id == destination.id, Route.is_active.is_(True))
        .first()
    )
    if not route:
        raise HTTPException(status_code=404, detail="Route distance is not configured")

    cab_rate = (
        db.query(CabRate)
        .filter(CabRate.cab_type == payload.cab_type, CabRate.is_active.is_(True))
        .first()
    )
    if not cab_rate:
        raise HTTPException(status_code=404, detail="Cab rate is not configured")

    room_query = db.query(HotelRoomRate).join(HiddenHotel).filter(
        HiddenHotel.destination_id == destination.id,
        HiddenHotel.is_active.is_(True),
        HotelRoomRate.category == payload.hotel_category,
        HotelRoomRate.is_active.is_(True),
    )
    if payload.hotel_option_id:
        room_query = room_query.filter(HotelRoomRate.id == payload.hotel_option_id)

    room_rate = room_query.order_by(HotelRoomRate.selling_price_per_room.asc()).first()
    if not room_rate:
        raise HTTPException(status_code=404, detail="Hotel category is not configured for this destination")

    return destination, route, cab_rate, room_rate


def calculate_estimate(db: Session, payload: EstimateRequest) -> EstimateResponse:
    destination, route, cab_rate, room_rate = get_rate_selection(db, payload)
    rooms = ceil(payload.tourists / TOURISTS_PER_ROOM)
    cab_total = (route.distance_km * cab_rate.rate_per_km) + (
        cab_rate.driver_allowance_per_day * payload.stay_days
    )
    hotel_total = room_rate.selling_price_per_room * rooms * payload.stay_days
    subtotal = cab_total + hotel_total + destination.base_package_price
    service_charge = subtotal * SERVICE_CHARGE_PERCENT / 100
    total_amount = subtotal + service_charge
    advance_amount = total_amount * ADVANCE_PERCENT / 100

    return EstimateResponse(
        destination_id=destination.id,
        tour=destination.name,
        hotel=payload.hotel_category,
        hotel_option_id=room_rate.id,
        display_name=public_hotel_display_name(
            room_rate.category.value,
            hotel_option_number(db, room_rate),
        ),
        cab=payload.cab_type,
        days=payload.stay_days,
        tourists=payload.tourists,
        rooms=rooms,
        distance_km=round(route.distance_km, 2),
        cab_total=round(cab_total, 2),
        hotel_total=round(hotel_total, 2),
        service_charge=round(service_charge, 2),
        total_amount=round(total_amount, 2),
        advance_payment_amount=round(advance_amount, 2),
    )


def available_hotel_categories(db: Session, destination_id: int | None = None) -> list[HotelCategory]:
    query = db.query(HotelRoomRate.category).join(HiddenHotel).filter(
        HiddenHotel.is_active.is_(True),
        HotelRoomRate.is_active.is_(True),
    )
    if destination_id:
        query = query.filter(HiddenHotel.destination_id == destination_id)
    return sorted({row[0] for row in query.all()}, key=lambda value: list(HotelCategory).index(value))


def available_cab_types(db: Session) -> list[CabRate]:
    return db.query(CabRate).filter(CabRate.is_active.is_(True)).all()
