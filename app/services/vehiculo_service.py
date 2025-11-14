# services/vehiculo_service.py
from sqlalchemy.orm import Session
from typing import List, Dict
from models.Vehiculo import Vehiculo

class VehiculoService:
    def __init__(self, db: Session):
        self.db = db

    def options(self) -> List[Dict]:
        q = self.db.query(Vehiculo).order_by(Vehiculo.placa.asc()).all()
        return [{"id": v.id, "placa": v.placa, "capacidad": v.capacidad} for v in q]
