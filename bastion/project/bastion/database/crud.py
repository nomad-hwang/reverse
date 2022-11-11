from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from bastion.database.database import Base

ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model: Type[ModelT]):
        self._model = model

    def get(self, db: Session, id: int) -> ModelT | None:
        return db.query(self._model).filter(self._model.id == id).first()

    def gets(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelT]:
        return db.query(self._model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaT) -> ModelT:
        db_obj = self._model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelT, obj_in: UpdateSchemaT | dict
    ) -> ModelT:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelT:
        obj = db.query(self._model).get(id)
        db.delete(obj)
        db.commit()
        return obj
