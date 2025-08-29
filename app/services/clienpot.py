# services/clienpot.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any, Optional
from models.Clienpot import Clientespot as ClipotModel
from schemas.Clienpot import CliPotCreate, Clipot as ClipotSchema

class ClipotService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Lecturas ----------
    def get_clipots(self) -> List[Dict[str, Any]]:
        q = self.db.query(ClipotModel).order_by(ClipotModel.razonSocial.asc())
        return [self._to_dict(x) for x in q.all()]

    def get_clipot(self, clipot_id: int) -> Optional[Dict[str, Any]]:
        x = self.db.query(ClipotModel).filter(ClipotModel.id == clipot_id).first()
        return self._to_dict(x) if x else None

    def get_by_nit(self, nit: str) -> Optional[Dict[str, Any]]:
        x = self.db.query(ClipotModel).filter(ClipotModel.nit == nit).first()
        return self._to_dict(x) if x else None

    # ---------- Creación ----------
    def create_clipot(self, payload: CliPotCreate) -> Dict[str, Any]:
        obj = ClipotModel(**payload.model_dump(exclude_unset=True))
        self.db.add(obj)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            # Relevamos al router para formatear HTTP 409
            raise e
        self.db.refresh(obj)
        return self._to_dict(obj)

    def create_from_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = ClipotModel(**data)
        self.db.add(obj)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise e
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ---------- Actualización ----------
    def update_clipot(self, clipot_id: int, payload: ClipotSchema) -> Optional[Dict[str, Any]]:
        obj = self.db.query(ClipotModel).filter(ClipotModel.id == clipot_id).first()
        if not obj:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise e
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update_from_dict(self, clipot_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        obj = self.db.query(ClipotModel).filter(ClipotModel.id == clipot_id).first()
        if not obj:
            return None
        for k, v in data.items():
            setattr(obj, k, v)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise e
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ---------- Borrado ----------
    def delete_clipot(self, clipot_id: int) -> bool:
        obj = self.db.query(ClipotModel).filter(ClipotModel.id == clipot_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ---------- Serializador ----------
    def _to_dict(self, x: Optional[ClipotModel]) -> Optional[Dict[str, Any]]:
        if not x:
            return None
        return {
            "id": x.id,
            "razonSocial": x.razonSocial,
            "nit": x.nit,
            "direccion": x.direccion,
            "telefono": x.telefono,
            "ciudad": x.ciudad,
            "contacto": x.contacto,
            "telefonoContacto": x.telefonoContacto,
            "actividad": x.actividad,
            "email": x.email,
            "observaciones": x.observaciones,
        }
