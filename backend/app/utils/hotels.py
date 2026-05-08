import json

from sqlalchemy.orm import Session

from app.models.catalog import HiddenHotel, HotelRoomRate
from app.schemas.catalog import HiddenHotelResponse, PublicHotelOption


def encode_amenities(amenities: list[str] | None) -> str:
    return json.dumps(amenities or [])


def decode_amenities(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return [item.strip() for item in value.split(",") if item.strip()]


def hotel_distance_km(hotel: HiddenHotel) -> float:
    return float(getattr(hotel, "distance_from_destination_km", 0.0) or 0.0)


def hidden_hotel_response(hotel: HiddenHotel) -> HiddenHotelResponse:
    return HiddenHotelResponse(
        id=hotel.id,
        destination_id=hotel.destination_id,
        owner_id=hotel.owner_id,
        owner_name=hotel.owner.owner_name if hotel.owner else None,
        real_hotel_name=hotel.real_hotel_name,
        address=hotel.address,
        nearby_place=hotel.nearby_place,
        distance_from_destination_km=hotel_distance_km(hotel),
        amenities=decode_amenities(hotel.amenities),
        check_in_time=hotel.check_in_time,
        check_out_time=hotel.check_out_time,
        is_active=hotel.is_active,
        created_at=hotel.created_at,
        updated_at=hotel.updated_at,
    )


def public_hotel_display_name(category_value: str, option_number: int) -> str:
    return f"{category_value} Hotel Option {option_number}"


def hotel_option_number(db: Session, rate: HotelRoomRate) -> int:
    rates = (
        db.query(HotelRoomRate)
        .join(HiddenHotel)
        .filter(
            HiddenHotel.destination_id == rate.hotel.destination_id,
            HiddenHotel.is_active.is_(True),
            HotelRoomRate.category == rate.category,
            HotelRoomRate.is_active.is_(True),
        )
        .order_by(
            HotelRoomRate.selling_price_per_room.asc(),
            HotelRoomRate.id.asc(),
        )
        .all()
    )
    for index, available_rate in enumerate(rates, start=1):
        if available_rate.id == rate.id:
            return index
    return 1


def public_hotel_option(rate: HotelRoomRate, option_number: int) -> PublicHotelOption:
    hotel = rate.hotel
    return PublicHotelOption(
        hotel_option_id=rate.id,
        destination_id=hotel.destination_id,
        category=rate.category,
        display_name=public_hotel_display_name(rate.category.value, option_number),
        selling_price_per_room=rate.selling_price_per_room,
        rooms_available=rate.rooms_available,
        nearby_place=hotel.nearby_place,
        distance_from_tour_km=hotel_distance_km(hotel),
        amenities=decode_amenities(hotel.amenities),
        check_in_time=hotel.check_in_time,
        check_out_time=hotel.check_out_time,
    )
