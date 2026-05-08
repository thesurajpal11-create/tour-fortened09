from app.auth.security import hash_password
from app.models import *  # noqa: F403
from app.models.catalog import CabRate, CabType, HiddenHotel, HotelCategory, HotelOwner, HotelRoomRate, Route
from app.models.destination import Destination
from app.models.user import User, UserRole
from app.utils import encode_amenities
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

DESTINATIONS = [
    ("Ayodhya", 0, 2500, "Holy birthplace of Lord Ram with the magnificent Ram Mandir."),
    ("Varanasi", 220, 3500, "Spiritual heart of India with sacred Ganges ghats and evening aarti."),
    ("Prayagraj", 165, 3000, "Sacred Sangam city where the Ganga, Yamuna, and Saraswati meet."),
    ("Chitrakoot", 275, 3200, "Lord Ram's forest retreat with temples, ghats, and quiet hills."),
    ("Vindhyachal", 250, 3100, "Powerful Shakti Peeth pilgrimage destination near Mirzapur."),
    ("Mathura", 530, 4200, "Sacred birthplace of Lord Krishna with temples and Braj culture."),
]

CAB_RATES = [
    (CabType.SEDAN, 14, 500, 4),
    (CabType.SUV, 18, 700, 6),
    (CabType.INNOVA, 22, 800, 7),
    (CabType.TEMPO_TRAVELLER, 35, 1200, 12),
]

HOTEL_RATE_MAP = {
    HotelCategory.BUDGET: (900, 1300),
    HotelCategory.TWO_STAR: (1400, 1900),
    HotelCategory.THREE_STAR: (2200, 3000),
    HotelCategory.FOUR_STAR: (3600, 4800),
}


def upsert_seed_data():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@ramnagari.com").first()
        if not admin:
            admin = User(
                name="Ramnagari Admin",
                email="admin@ramnagari.com",
                phone="9000000000",
                role=UserRole.ADMIN,
                hashed_password=hash_password("Admin@123"),
            )
            db.add(admin)

        owner_user = db.query(User).filter(User.email == "owner@ramnagari.com").first()
        if not owner_user:
            owner_user = User(
                name="Sample Hotel Owner",
                email="owner@ramnagari.com",
                phone="9111111111",
                role=UserRole.HOTEL_OWNER,
                hashed_password=hash_password("Owner@123"),
            )
            db.add(owner_user)
            db.flush()

        owner = db.query(HotelOwner).filter(HotelOwner.email == "owner@ramnagari.com").first()
        if not owner:
            owner = HotelOwner(
                user_id=owner_user.id,
                owner_name="Sample Hotel Group",
                email="owner@ramnagari.com",
                phone="9111111111",
            )
            db.add(owner)
            db.flush()

        destination_by_name = {}
        for name, distance, package_price, summary in DESTINATIONS:
            destination = db.query(Destination).filter(Destination.name == name).first()
            if not destination:
                destination = Destination(
                    name=name,
                    description=f"{summary} Ramnagari Tourism offers curated pilgrimage travel support for this destination.",
                    short_description=summary,
                    image_url=f"/images/{name.lower()}.jpg",
                    base_package_price=package_price,
                    best_time_to_visit="October to March",
                )
                db.add(destination)
                db.flush()
            destination_by_name[name] = destination

            route = db.query(Route).filter(Route.origin == "Ayodhya", Route.destination_id == destination.id).first()
            if not route:
                db.add(Route(origin="Ayodhya", destination_id=destination.id, distance_km=distance))

            hotel = db.query(HiddenHotel).filter(
                HiddenHotel.destination_id == destination.id,
                HiddenHotel.real_hotel_name == f"{name} Heritage Stay",
            ).first()
            if not hotel:
                hotel = HiddenHotel(
                    destination_id=destination.id,
                    owner_id=owner.id,
                    real_hotel_name=f"{name} Heritage Stay",
                    address=f"Central {name}",
                    nearby_place=f"Near {name} main temple area",
                    distance_from_destination_km=1.8 if name == "Ayodhya" else 3.5,
                    amenities=encode_amenities(["AC Room", "WiFi", "Parking", "Breakfast", "Hot Water"]),
                    check_in_time="12:00 PM",
                    check_out_time="11:00 AM",
                )
                db.add(hotel)
                db.flush()

            for category, (base_price, selling_price) in HOTEL_RATE_MAP.items():
                rate = db.query(HotelRoomRate).filter(
                    HotelRoomRate.hotel_id == hotel.id,
                    HotelRoomRate.category == category,
                ).first()
                if not rate:
                    db.add(
                        HotelRoomRate(
                            hotel_id=hotel.id,
                            category=category,
                            base_price_per_room=base_price,
                            selling_price_per_room=selling_price,
                            rooms_available=20,
                        )
                    )

        for cab_type, rate_per_km, allowance, capacity in CAB_RATES:
            cab_rate = db.query(CabRate).filter(CabRate.cab_type == cab_type).first()
            if not cab_rate:
                db.add(
                    CabRate(
                        cab_type=cab_type,
                        rate_per_km=rate_per_km,
                        driver_allowance_per_day=allowance,
                        capacity=capacity,
                    )
                )

        db.commit()
        print("Seed data added: destinations, routes, cab rates, hidden hotels, room rates, admin, hotel owner.")
        print("Admin login: admin@ramnagari.com / Admin@123")
        print("Hotel owner login: owner@ramnagari.com / Owner@123")
    finally:
        db.close()


if __name__ == "__main__":
    upsert_seed_data()
