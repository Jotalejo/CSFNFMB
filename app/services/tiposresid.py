# services/tiposresid.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from models.TipoResiduo import TipoResiduo as TipoResidModel
from schemas.Tiporesid import TipoResidCreate, TipoResidOut

class TipoResidService:
    def __init__(self, db: Session):
        self.db = db

    # ------- Lecturas -------
    def list_all(self) -> List[Dict[str, Any]]:
        q = self.db.query(TipoResidModel).order_by(TipoResidModel.nombre.asc())
        return [self._to_dict(x) for x in q.all()]

    def get_by_id(self, tipores_id: int) -> Optional[Dict[str, Any]]:
        obj = self.db.query(TipoResidModel).filter(TipoResidModel.id == tipores_id).first()
        return self._to_dict(obj) if obj else None

    # ------- Crear / Actualizar -------
    def create(self, payload: TipoResidCreate) -> Dict[str, Any]:
        obj = TipoResidModel(**payload.model_dump(exclude_unset=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, tipores_id: int, payload: TipoResidOut) -> Optional[Dict[str, Any]]:
        obj = self.db.query(TipoResidModel).filter(TipoResidModel.id == tipores_id).first()
        if not obj:
            return None
        for field, val in payload.model_dump(exclude_unset=True).items():
            if field == "id":
                continue
            setattr(obj, field, val)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ------- Borrar -------
    def delete(self, tipores_id: int) -> bool:
        obj = self.db.query(TipoResidModel).filter(TipoResidModel.id == tipores_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ------- Utilidad -------
    def _to_dict(self, x: Optional[TipoResidModel]) -> Optional[Dict[str, Any]]:
        if not x:
            return None
        return {
            "id": x.id,
            "nombre": x.nombre,
            "clasificacion": x.clasificacion,
            "observaciones": x.observaciones,
        }
