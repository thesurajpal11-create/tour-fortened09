from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.catalog import HiddenHotel, HotelCategory, HotelRoomRate
from app.models.destination import Destination
from app.schemas.booking import EstimateRequest, EstimateResponse
from app.schemas.catalog import PublicCabType, PublicHotelOption, PublicHotelType, PublicTourPackage
from app.schemas.destination import DestinationResponse
from app.services.pricing import available_cab_types, available_hotel_categories, calculate_estimate
from app.utils import public_hotel_option
from database import get_db


router = APIRouter(prefix="/api/catalog", tags=["Public Catalog"])


@router.get("/destinations", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    return db.query(Destination).filter(Destination.is_active.is_(True)).all()


@router.get("/tour-packages", response_model=list[PublicTourPackage])
def list_tour_packages(db: Session = Depends(get_db)):
    destinations = db.query(Destination).filter(Destination.is_active.is_(True)).all()
    return [
        {
            "destination_id": destination.id,
            "tour": destination.name,
            "short_description": destination.short_description,
            "base_package_price": destination.base_package_price,
            "best_time_to_visit": destination.best_time_to_visit,
        }
        for destination in destinations
    ]


@router.get("/hotel-types", response_model=list[PublicHotelType])
def list_hotel_types(destination_id: int | None = None, db: Session = Depends(get_db)):
    categories = available_hotel_categories(db, destination_id)
    if not categories:
        categories = list(HotelCategory)
    return [{"category": category, "display_name": category.value} for category in categories]


@router.get("/hotel-options", response_model=list[PublicHotelOption])
def list_hotel_options(
    destination_id: int,
    category: HotelCategory | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(HotelRoomRate).join(HiddenHotel).filter(
        HiddenHotel.destination_id == destination_id,
        HiddenHotel.is_active.is_(True),
        HotelRoomRate.is_active.is_(True),
    )
    if category:
        query = query.filter(HotelRoomRate.category == category)

    rates = query.order_by(
        HotelRoomRate.category.asc(),
        HotelRoomRate.selling_price_per_room.asc(),
        HotelRoomRate.id.asc(),
    ).all()

    category_counts = {}
    options = []
    for rate in rates:
        category_counts[rate.category] = category_counts.get(rate.category, 0) + 1
        options.append(public_hotel_option(rate, category_counts[rate.category]))
    return options


@router.get("/cab-types", response_model=list[PublicCabType])
def list_cab_types(db: Session = Depends(get_db)):
    return available_cab_types(db)


@router.post("/estimate", response_model=EstimateResponse)
def estimate(payload: EstimateRequest, db: Session = Depends(get_db)):
    return calculate_estimate(db, payload)
