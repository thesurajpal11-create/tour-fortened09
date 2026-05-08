from sqlalchemy import inspect, text


def add_missing_columns(engine, table_name: str, required_columns: dict[str, str]) -> None:
    inspector = inspect(engine)
    existing_columns = {
        column["name"]
        for column in inspector.get_columns(table_name)
    }
    missing_columns = [
        (name, definition)
        for name, definition in required_columns.items()
        if name not in existing_columns
    ]
    if not missing_columns:
        return

    with engine.begin() as connection:
        for name, definition in missing_columns:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN `{name}` {definition}"))


def ensure_catalog_schema(engine) -> None:
    add_missing_columns(
        engine,
        "destinations",
        {
            "base_package_price": "FLOAT NOT NULL DEFAULT 0",
            "is_active": "BOOLEAN NOT NULL DEFAULT TRUE",
        },
    )
    add_missing_columns(
        engine,
        "users",
        {
            "hashed_password": "VARCHAR(255) NULL",
            "role": "VARCHAR(20) NOT NULL DEFAULT 'customer'",
        },
    )
    add_missing_columns(
        engine,
        "hidden_hotels",
        {
            "nearby_place": "VARCHAR(160) NULL",
            "distance_from_destination_km": "FLOAT NOT NULL DEFAULT 0",
            "amenities": "TEXT NULL",
            "check_in_time": "VARCHAR(20) NOT NULL DEFAULT '12:00 PM'",
            "check_out_time": "VARCHAR(20) NOT NULL DEFAULT '11:00 AM'",
        },
    )
    add_missing_columns(
        engine,
        "bookings",
        {
            "booking_code": "VARCHAR(40) NULL",
            "route_id": "INT NULL",
            "hotel_room_rate_id": "INT NULL",
            "cab_rate_id": "INT NULL",
            "tourists": "INT NULL",
            "stay_days": "INT NULL",
            "rooms": "INT NULL",
            "distance_km": "FLOAT NULL",
            "cab_total": "FLOAT NULL",
            "hotel_total": "FLOAT NULL",
            "service_charge": "FLOAT NULL",
            "advance_amount": "FLOAT NULL",
            "payment_status": "VARCHAR(20) NOT NULL DEFAULT 'unpaid'",
        },
    )
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users MODIFY COLUMN `password` VARCHAR(255) NULL"))
        connection.execute(text("ALTER TABLE bookings MODIFY COLUMN `service_type` VARCHAR(100) NULL"))
        connection.execute(text("ALTER TABLE bookings MODIFY COLUMN `check_in_date` DATETIME NULL"))
        connection.execute(text("ALTER TABLE bookings MODIFY COLUMN `check_out_date` DATETIME NULL"))
        connection.execute(text("ALTER TABLE bookings MODIFY COLUMN `status` VARCHAR(30) NULL"))
