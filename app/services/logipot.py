# services/logipot.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import Logispot as LogiModel

class LogispotService:
    def __init__(self, db: Session):
        self.db = db

    def list_by_clipot(self, clipot_id: int) -> List[Dict[str, Any]]:
        q = self.db.query(LogiModel).filter(LogiModel.codclipot == clipot_id).order_by(LogiModel.id.desc())
        return [self._to_dict(x) for x in q.all()]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = LogiModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, logi_id: int, data: Dict[str, Any]) -> bool:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        if not obj: return False
        for k, v in data.items():
            setattr(obj, k, v)
        self.db.commit()
        return True

    def delete(self, logi_id: int) -> bool:
        obj = self.db.query(LogiModel).filter(LogiModel.id == logi_id).first()
        if not obj: return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def _to_dict(self, x: LogiModel) -> Dict[str, Any]:
        return {
            "id": x.id,
            "codclipot": x.codclipot,
            "frecuerec": x.frecuerec,
            "capavehic": x.capavehic,
            "distancia": x.distancia,
            "observaciones": x.observaciones,
        }
