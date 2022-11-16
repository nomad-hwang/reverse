from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class DictMixin:
    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# from sqlalchemy import MetaData
# POSTGRES_INDEXES_NAMING_CONVENTION = {
#     "ix": "%(column_0_label)s_idx",
#     "uq": "%(table_name)s_%(column_0_name)s_key",
#     "ck": "%(table_name)s_%(constraint_name)s_check",
#     "fk": "%(table_name)s_%(column_0_name)s_fkey",
#     "pk": "%(table_name)s_pkey",
# }
# metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
