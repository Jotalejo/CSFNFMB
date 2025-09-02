# services/logipot.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

# Ajusta el import a tu estructura:
from models.Logispot import Logispot as LogiModel
# Si usas prefijo de paquete: from app.models.Logispot import Logispot as LogiModel

from schemas.Logispot import LogiPotCreate, LogiPotOut

class LogiPotService:
    def __init__(self, db: Session):
        self.db = db

    # ------- Lecturas -------
    def list_by_clipot(self, clipot_id: int) -> List[Dict[str, Any]]:
        q = (self.db.query(LogiModel)
             .filter(LogiModel.codclipot == clipot_id)
             .order_by(LogiModel.id.desc()))
        return [self._to_dict(x) for x in q.all()]

    def get_by_id(self, logi_id: int) -> Optional[Dict[str, Any]]:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        return self._to_dict(obj) if obj else None

    # ------- Crear / Actualizar (JSON) -------
    def create(self, payload: LogiPotCreate) -> Dict[str, Any]:
        obj = LogiModel(**payload.model_dump(exclude_unset=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, logi_id: int, payload: LogiPotOut) -> Optional[Dict[str, Any]]:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        if not obj:
            return None
        for field, val in payload.model_dump(exclude_unset=True).items():
            if field == "id":
                continue
            setattr(obj, field, val)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ------- Crear / Actualizar (desde FORM del modal) -------
    def create_from_form(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        data keys esperadas: codclipot, frecuerec, capavehic, distancia, observaciones
        """
        obj = LogiModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update_from_form(self, logi_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        if not obj:
            return None
        for k, v in data.items():
            if k == "id":
                continue
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ------- Borrar -------
    def delete(self, logi_id: int) -> bool:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ------- Serializador -------
    def _to_dict(self, x: Optional[LogiModel]) -> Optional[Dict[str, Any]]:
        if not x:
            return None
        return {
            "id": x.id,
            "codclipot": x.codclipot,
            "frecuerec": x.frecuerec,
            "capavehic": x.capavehic,
            "distancia": x.distancia,
            "observaciones": x.observaciones,
        }
