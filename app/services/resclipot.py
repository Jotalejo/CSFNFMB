# services/resclipot.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from schemas import ResiduosCliCreate, ResiduosCliUpdate


# Usa el alias para dejar claro que es POT:
from models import ResiduosClientePotencial as ResiduosCliPotModel
# Si usas paquete "app", cambia a:
# from app.models.Residuoclipot import ResiduosCli as ResiduosCliPotModel

from schemas.Resclipot import ResiduosCliCreate, ResiduosCliUpdate


class ResCliPotService:
    def __init__(self, db: Session):
        self.db = db

    # -------- Lecturas --------
    def list_by_clipot(self, clipot_id: int) -> List[Dict[str, Any]]:
        q = (self.db.query(ResiduosCliPotModel)
             .filter(ResiduosCliPotModel.ccliente == clipot_id)
             .order_by(ResiduosCliPotModel.id.desc()))
        return [self._to_dict(x) for x in q.all()]

    def get_by_id(self, resid_id: int) -> Optional[Dict[str, Any]]:
        obj = self.db.query(ResiduosCliPotModel).filter(
            ResiduosCliPotModel.id == resid_id).first()
        return self._to_dict(obj) if obj else None

    # -------- Crear / Actualizar (JSON) --------
    def create(self, payload: ResiduosCliCreate) -> Dict[str, Any]:
        obj = ResiduosCliPotModel(**payload.model_dump(exclude_unset=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, resid_id: int, payload: ResiduosCliUpdate) -> Optional[Dict[str, Any]]:
        obj = self.db.query(ResiduosCliPotModel).filter(
            ResiduosCliPotModel.id == resid_id).first()
        if not obj:
            return None
        for field, val in payload.model_dump(exclude_unset=True).items():
            if field == "id":
                continue
            setattr(obj, field, val)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # -------- Crear / Actualizar (desde FORM del modal) --------
    def create_from_form(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = ResiduosCliPotModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update_from_form(self, resid_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        obj = self.db.query(ResiduosCliPotModel).filter(
            ResiduosCliPotModel.id == resid_id).first()
        if not obj:
            return None
        for k, v in data.items():
            if k == "id":
                continue
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # -------- Borrar --------
    def delete(self, resid_id: int) -> bool:
        obj = self.db.query(ResiduosCliPotModel).filter(
            ResiduosCliPotModel.id == resid_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # -------- Serializador --------
    def _to_dict(self, r: Optional[ResiduosCliPotModel]) -> Optional[Dict[str, Any]]:
        if not r:
            return None
        return {
            "id": r.id,
            "ccliente": r.ccliente,
            "tresiduo": r.tresiduo,
            "cantresiduo": r.cantresiduo,
            "pesopromres": r.pesopromres,
            "segregares": r.segregares,
            "numbolsas": r.numbolsas,
            "observaciones": r.observaciones,
        }
