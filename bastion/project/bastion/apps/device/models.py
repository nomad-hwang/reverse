from sqlalchemy import Column, String

from bastion.database.model import Base


class Device(Base):
    name = Column(String(255), unique=True, index=True)
    ssh_key = Column(String(255))
    alias = Column(String(50), nullable=True, index=True, unique=True)
