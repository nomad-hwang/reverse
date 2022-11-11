from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str
    ssh_key: str


class DeviceUpdate(BaseModel):
    ssh_key: str | None = None
    alias: str | None = None
    active: bool | None = None


class Device(BaseModel):
    name: str
    ssh_key: str
    alias: str | None
    active: bool
