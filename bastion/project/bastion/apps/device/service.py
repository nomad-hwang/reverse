from sqlalchemy.orm import Session

from bastion.apps.device.crud import DeviceCrud
from bastion.apps.device.schemas import Device, DeviceCreate, DeviceUpdate


class DeviceService(object):
    def __init__(self):
        self._crud = DeviceCrud()

    def create_device(self, db: Session, *, dto: DeviceCreate) -> Device:
        return self._crud.create(db, dto=dto)

    def update_device(self, db: Session, *, name: str, dto: DeviceUpdate) -> Device:
        return self._crud.update(db, name=name, obj_in=dto)

    def set_ssh_key(self, db: Session, *, name: str, ssh_key: str) -> None:
        self._crud.update(db, name=name, obj_in=DeviceUpdate(ssh_key=ssh_key))

    def set_active(self, db: Session, *, name: str, active: bool) -> None:
        self._crud.update(db, name=name, obj_in=DeviceUpdate(active=active))

    def get_device(self, db: Session, *, name: str) -> Device:
        return self._crud.get_by_name(db, name=name)

    def get_all_devices(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Device]:
        return self._crud.gets(db, skip=skip, limit=limit)
