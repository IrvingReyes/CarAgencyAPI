from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, col, func, select

from app.database import SessionDep
from app.dependencies import get_current_user
from app.models import VehicleDB
from app.schemas.vehicle import (
    Vehicle,
    VehicleConditionUpdate,
    VehicleConditionUpdateResponse,
    VehicleCreate,
    VehicleFilters,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[Vehicle])
def list_vehicles(session: SessionDep, filters: Annotated[VehicleFilters, Query()]):
    query = select(VehicleDB)
    if filters.brand is not None:
        query = query.where(func.lower(VehicleDB.brand) == filters.brand.lower())
    if filters.available is not None:
        query = query.where(VehicleDB.available == filters.available)
    if filters.sold is not None:
        query = query.where(VehicleDB.sold == filters.sold)
    if filters.condition:
        query = query.where(col(VehicleDB.condition).in_(filters.condition))
    if filters.min_price is not None:
        query = query.where(VehicleDB.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.where(VehicleDB.price <= filters.max_price)
    return session.exec(query.order_by(VehicleDB.id)).all()


@router.get("/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int, session: SessionDep):
    return find_vehicle(session, vehicle_id)


@router.post("/", response_model=Vehicle, status_code=201, dependencies=[Depends(get_current_user)])
def create_vehicle(payload: VehicleCreate, session: SessionDep):
    vehicle = VehicleDB(**payload.model_dump(exclude={"images"}))
    # HttpUrl is not JSON serializable, so store the images in JSON mode
    vehicle.images = payload.images.model_dump(mode="json")
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.put(
    "/{vehicle_id}/condition",
    response_model=VehicleConditionUpdateResponse,
    dependencies=[Depends(get_current_user)],
)
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
