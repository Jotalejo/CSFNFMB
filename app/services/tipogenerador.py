# services/tipogenerador.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from models import TipoGen as TipoGeneradorModel  # el model se llama TipoGen

class TipoGeneradorService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Dict[str, Any]]:
        q = self.db.query(TipoGeneradorModel).order_by(TipoGeneradorModel.nombre.asc())
        return [
            {"id": x.id, "nombre": x.nombre, "tamax": x.tamax, "tamin": x.tamin, "observaciones": x.observaciones}
            for x in q.all()
        ]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = TipoGeneradorModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return {
            "id": obj.id, "nombre": obj.nombre,
            "tamax": obj.tamax, "tamin": obj.tamin, "observaciones": obj.observaciones
        }

    def update(self, tid: int, data: Dict[str, Any]) -> bool:
        obj = self.db.query(TipoGeneradorModel).filter(TipoGeneradorModel.id == tid).first()
        if not obj: return False
        for k, v in data.items():
            if v is not None:
                setattr(obj, k, v)
        self.db.commit()
        return True

    def delete(self, tid: int) -> bool:
        obj = self.db.query(TipoGeneradorModel).filter(TipoGeneradorModel.id == tid).first()
        if not obj: return False
        self.db.delete(obj)
        self.db.commit()
        return True
