# services/tiposvisita.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from models import TipoVisita as TipoVisitaModel

class TipoVisitaService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Dict[str, Any]]:
        q = self.db.query(TipoVisitaModel).order_by(TipoVisitaModel.nombre.asc())
        return [{"id": x.id, "nombre": x.nombre, "observaciones": x.observaciones} for x in q.all()]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = TipoVisitaModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return {"id": obj.id, "nombre": obj.nombre, "observaciones": obj.observaciones}

    def update(self, tipovis_id: int, data: Dict[str, Any]) -> bool:
        obj = self.db.query(TipoVisitaModel).filter(TipoVisitaModel.id == tipovis_id).first()
        if not obj: return False
        if data.get("nombre") is not None: obj.nombre = data["nombre"]
        if data.get("observaciones") is not None: obj.observaciones = data["observaciones"]
        self.db.commit()
        return True

    def delete(self, tipovis_id: int) -> bool:
        obj = self.db.query(TipoVisitaModel).filter(TipoVisitaModel.id == tipovis_id).first()
        if not obj: return False
        self.db.delete(obj)
        self.db.commit()
        return True
