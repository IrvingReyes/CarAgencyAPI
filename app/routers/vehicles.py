from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, col, func, select

from app.database import SessionDep
from app.models import VehicleDB
from app.schemas.vehicle import (
    Vehicle,
    VehicleCondition,
    VehicleConditionUpdate,
    VehicleConditionUpdateResponse,
    VehicleCreate,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[Vehicle])
def list_vehicles(
    session: SessionDep,
    brand: str | None = None,
    available: bool | None = None,
    sold: bool | None = None,
    condition: list[VehicleCondition] | None = Query(default=None),
):
    query = select(VehicleDB)
    if brand is not None:
        query = query.where(func.lower(VehicleDB.brand) == brand.lower())
    if available is not None:
        query = query.where(VehicleDB.available == available)
    if sold is not None:
        query = query.where(VehicleDB.sold == sold)
    if condition:
        query = query.where(col(VehicleDB.condition).in_(condition))
    return session.exec(query.order_by(VehicleDB.id)).all()


@router.get("/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int, session: SessionDep):
    return find_vehicle(session, vehicle_id)


@router.post("/", response_model=Vehicle, status_code=201)
def create_vehicle(payload: VehicleCreate, session: SessionDep):
    vehicle = VehicleDB(**payload.model_dump())
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.put("/{vehicle_id}/condition", response_model=VehicleConditionUpdateResponse)
def update_vehicle_condition(vehicle_id: int, payload: VehicleConditionUpdate, session: SessionDep):
    vehicle = find_vehicle(session, vehicle_id)
    if vehicle.condition == payload.condition:
        message = f"Vehicle {vehicle_id} was already in condition '{payload.condition.value}'"
    else:
        message = (
            f"Vehicle {vehicle_id} condition updated from "
            f"'{vehicle.condition.value}' to '{payload.condition.value}'"
        )
        vehicle.condition = payload.condition
        session.add(vehicle)
        session.commit()
        session.refresh(vehicle)
    return VehicleConditionUpdateResponse(message=message, vehicle=vehicle)


def find_vehicle(session: Session, vehicle_id: int) -> VehicleDB:
    vehicle = session.get(VehicleDB, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
