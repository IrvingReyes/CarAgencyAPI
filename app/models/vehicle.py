from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import Field, SQLModel

from app.schemas.vehicle import VehicleCondition


class VehicleDB(SQLModel, table=True):
    __tablename__ = "vehicle"
    __table_args__ = (
        # ADR 0001: a sold vehicle is never available for sale.
        sa.CheckConstraint("NOT (sold AND available)", name="sold_vehicle_not_available"),
    )

    id: int | None = Field(default=None, primary_key=True)
    brand: str = Field(index=True)
    model: str
    year: int
    color: str
    mileage: int
    price: Decimal = Field(sa_column=sa.Column(sa.Numeric(12, 2), nullable=False))
    condition: VehicleCondition = Field(
        sa_column=sa.Column(
            sa.Enum(
                VehicleCondition,
                name="vehicle_condition",
                values_callable=lambda enum: [member.value for member in enum],
            ),
            nullable=False,
            index=True,
        )
    )
    known_issues: list[str] = Field(
        default_factory=list,
        sa_column=sa.Column(ARRAY(sa.String), nullable=False, server_default="{}"),
    )
    available: bool = True
    sold: bool = False
    location: str | None = None
    observation: str | None = None
    # Serialized VehicleImages: {"main_image": ..., "image_carousel": [...], "image_to_fix": [...]}
    images: dict = Field(
        default_factory=dict,
        sa_column=sa.Column(JSONB, nullable=False, server_default="{}"),
    )
