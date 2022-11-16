from bastion.apps.device.router import api_router as device_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(device_router, prefix="/api/v1/device", tags=["device"])
