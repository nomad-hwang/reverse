from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from bastion.apps.device.schemas import Device, DeviceCreate, DeviceUpdate
from bastion.apps.device.service import DeviceService
from bastion.database.database import get_db

api_router = APIRouter()


@api_router.get("", response_model=List[Device])
def get_devices(db: Session = Depends(get_db)):
    return DeviceService().get_all_devices(db)


@api_router.post("", status_code=status.HTTP_201_CREATED, response_model=Device)
def create_device(request: DeviceCreate, db: Session = Depends(get_db)):
    return DeviceService().create_device(db, dto=request)


@api_router.get("/{name}", status_code=status.HTTP_200_OK, response_model=Device)
def get(name: str, db: Session = Depends(get_db)):
    return DeviceService().get_device(db, name=name)


@api_router.put("/{name}", status_code=status.HTTP_200_OK, response_model=Device)
def update(name: str, request: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService().update_device(db, name=name, dto=request)
