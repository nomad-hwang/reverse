from bastion.apps.device.linux_user.exceptions import UserExists, UserNotFound
from bastion.apps.device.linux_user.service import LinuxUserService
from bastion.apps.device.models import Device as DeviceORM
from bastion.apps.device.schemas import Device, DeviceCreate, DeviceUpdate
from bastion.database.crud import CRUDBase
from sqlalchemy.orm import Session


class DeviceCrud(CRUDBase[DeviceORM, DeviceCreate, DeviceUpdate]):
    def __init__(self):
        super().__init__(DeviceORM)
        self._linux = LinuxUserService()

    def create(self, db: Session, *, dto: DeviceCreate) -> DeviceORM:
        try:
            ret = super().create(db, obj_in=dto)
            self._linux.create(dto.name, dto.ssh_key)
            return ret
        except:
            if not self._linux.user_exists(dto.name):
                self._linux.create(dto.name, dto.ssh_key)
            raise UserExists

    def get_by_name(self, db: Session, *, name: str) -> DeviceORM:
        ret = db.query(self._model).filter(self._model.name == name).first()
        if ret is None:
            raise UserNotFound
        self._sync(ret)
        return ret

    def get_by_alias(self, db: Session, *, alias: str) -> DeviceORM:
        ret = db.query(self._model).filter(self._model.alias == alias).first()
        if ret is None:
            raise UserNotFound
        self._sync(ret)
        return ret

    def update(self, db: Session, *, name: str, obj_in: DeviceUpdate) -> DeviceORM:
        return super().update(db, db_obj=self.get_by_name(db, name=name), obj_in=obj_in)

    def _sync(self, device: Device | None) -> None:
        if not device:
            return
        if self._linux.user_exists(device.name) == False:
            self._linux.create(device.name, device.ssh_key, device.active)
        if self._linux.get_ssh_key(device.name) != device.ssh_key:
            self._linux.update_ssh_key(device.name, device.ssh_key)
        if self._linux.active(device.name) != device.active:
            self._linux.update_active(device.name, device.active)
