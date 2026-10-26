from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class VehicleCondition(str, Enum):
    OPERATIONAL = "operational"
    NEEDS_REPAIR = "needs_repair"
    IN_REPAIR = "in_repair"
    PARTS_ONLY = "parts_only"


class VehicleImages(BaseModel):
    main_image: HttpUrl | None = None
    image_carousel: list[HttpUrl] = []
    image_to_fix: list[HttpUrl] = []


class VehicleCreate(BaseModel):
    brand: str
    model: str
    year: int = Field(ge=1900, le=2100)
    color: str
    mileage: int = Field(ge=0)
    price: float = Field(gt=0)
    condition: VehicleCondition
    known_issues: list[str] = []
    available: bool = True
    sold: bool = False
    location: str | None = None
    observation: str | None = None
    images: VehicleImages = Field(default_factory=VehicleImages)
    # # Service information
    # service_product_id: int | None = None
    # brand_id: int | None = None
    # service_comment: str | None = None
    # # Vehicle information
    # vehicle_brand_id: int | None = None
    # vehicle_model_id: int | None = None
    # color: str | None = None
    # vin_sn: str | None = None
    # odometer: str | None = None
    # license_plate: str | None = None
    # # Vehicle bools
    # radio: bool | None = None
    # air_booler: bool | None = None
    # electric_locks: bool | None = None
    # electric_windows: bool | None = None
    # horn: bool | None = None
    # vehicle_ignition: bool | None = None
    # lights: bool | None = None
    # # Vehicle accessories
    # mirrors: bool = False
    # fire_extinguisher: bool = False
    # first_aid_kit: bool = False
    # carpet: bool = False
    # wiper_washer: bool = False
    # jack: bool = False
    # spare_tire: bool = False

    @model_validator(mode="after")
    def sold_vehicles_are_not_available(self):
        # ADR 0001: a sold vehicle is never available for sale.
        if self.sold:
            self.available = False
        return self


class Vehicle(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class VehicleConditionUpdate(BaseModel):
    condition: VehicleCondition


class VehicleConditionUpdateResponse(BaseModel):
    message: str
    vehicle: Vehicle


class VehicleFilters(BaseModel):
    """Search filters for GET /vehicles/, received as query parameters."""

    brand: str | None = None
    available: bool | None = None
    sold: bool | None = None
    condition: list[VehicleCondition] | None = None
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def price_range_is_valid(self):
        if self.min_price is not None and self.max_price is not None and self.min_price > self.max_price:
            raise ValueError("min_price must be less than or equal to max_price")
        return self
