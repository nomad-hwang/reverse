from email.policy import default

from bastion.database.model import Base, DictMixin
from sqlalchemy import Boolean, Column, String


class Device(Base, DictMixin):
    name = Column(String(255), unique=True, index=True)
    ssh_key = Column(String(255))
    alias = Column(String(50), nullable=True, index=True, unique=True)
    active = Column(Boolean, default=True)
