from bastion.apps.device.crud import DeviceCrud
from bastion.apps.device.schemas import Device, DeviceCreate, DeviceUpdate
from sqlalchemy.orm import Session


class DeviceService(object):
    def __init__(self):
        self._crud = DeviceCrud()

    def create_device(self, db: Session, *, dto: DeviceCreate) -> Device:
        return Device(**self._crud.create(db, dto=dto).dict())

    def update_device(self, db: Session, *, name: str, dto: DeviceUpdate) -> Device:
        return Device(**self._crud.update(db, name=name, obj_in=dto).dict())

    def set_ssh_key(self, db: Session, *, name: str, ssh_key: str) -> None:
        self._crud.update(db, name=name, obj_in=DeviceUpdate(ssh_key=ssh_key))

    def set_active(self, db: Session, *, name: str, active: bool) -> None:
        self._crud.update(db, name=name, obj_in=DeviceUpdate(active=active))

    def get_device(self, db: Session, *, name: str) -> Device:
        return self._crud.get_by_name(db, name=name)

    def get_all_devices(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Device]:
        return [Device(**x.dict()) for x in self._crud.gets(db, skip=skip, limit=limit)]
