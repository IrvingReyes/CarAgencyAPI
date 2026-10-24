"""Load sample vehicles for the showcase. Does nothing if the table already has data."""

from sqlmodel import Session, select

from app.database import engine
from app.models import VehicleDB
from app.schemas.vehicle import VehicleCondition

SAMPLE_VEHICLES = [
    VehicleDB(
        brand="Toyota", model="Corolla", year=2019, color="White", mileage=78000,
        price=249900, condition=VehicleCondition.OPERATIONAL,
        location="Monterrey Downtown",
    ),
    VehicleDB(
        brand="Nissan", model="Versa", year=2017, color="Gray", mileage=132000,
        price=89900, condition=VehicleCondition.NEEDS_REPAIR,
        known_issues=["Transmission slipping", "A/C not working"], location="Monterrey Downtown",
    ),
    VehicleDB(
        brand="Mazda", model="CX-5", year=2018, color="Red", mileage=95000,
        price=289900, condition=VehicleCondition.IN_REPAIR,
        known_issues=["Brake pads replacement"], location="San Nicolas Workshop",
    ),
    VehicleDB(
        brand="Volkswagen", model="Jetta", year=2014, color="Black", mileage=210000,
        price=35000, condition=VehicleCondition.PARTS_ONLY,
        known_issues=["Blown engine", "Front-end collision damage"], location="San Nicolas Workshop",
    ),
    VehicleDB(
        brand="Honda", model="Civic", year=2020, color="Blue", mileage=54000,
        price=319900, condition=VehicleCondition.OPERATIONAL, available=False,
        location="Monterrey Downtown",
    ),
]


def seed() -> None:
    with Session(engine) as session:
        if session.exec(select(VehicleDB)).first() is not None:
            print("Seed skipped: vehicles table already has data")
            return
        session.add_all(SAMPLE_VEHICLES)
        session.commit()
        print(f"Seeded {len(SAMPLE_VEHICLES)} vehicles")


if __name__ == "__main__":
    seed()
