from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from bastion.config import settings

engine = create_engine(
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# from sqlalchemy import MetaData
# POSTGRES_INDEXES_NAMING_CONVENTION = {
#     "ix": "%(column_0_label)s_idx",
#     "uq": "%(table_name)s_%(column_0_name)s_key",
#     "ck": "%(table_name)s_%(constraint_name)s_check",
#     "fk": "%(table_name)s_%(column_0_name)s_fkey",
#     "pk": "%(table_name)s_pkey",
# }
# metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
