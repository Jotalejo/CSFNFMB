# services/frecuencia_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from models.FrecuenciaRec import FrecuenciaRec
from models.TipoFrecuencia import TipoFrecuencia
from schemas.Frecuencia import FrecuenciaCreate, FrecuenciaUpdate

class FrecuenciaService:
    def __init__(self, db: Session):
        self.db = db

    def _tipo_id(self, nombre: str) -> int:
        tf = self.db.query(TipoFrecuencia).filter(TipoFrecuencia.nombre == nombre).first()
        if not tf:
            raise ValueError(f"Tipo de frecuencia '{nombre}' no existe")
        return tf.id

    def list_by_cliente(self, cliente_id: int) -> List[FrecuenciaRec]:
        return (
            self.db.query(FrecuenciaRec)
            .filter(FrecuenciaRec.cliente_id == cliente_id, FrecuenciaRec.activo == 1)
            .order_by(FrecuenciaRec.id.desc())
            .all()
        )

    def create(self, data: FrecuenciaCreate) -> FrecuenciaRec:
        tipo_id = self._tipo_id(data.tipo_nombre)

        diasem_mask = None
        if data.tipo_nombre in ("diaria", "semanal"):
            dias = data.dias_semana or (list(range(1,8)) if data.tipo_nombre=="diaria" else [])
            diasem_mask = FrecuenciaRec.to_mask(dias)

        rec = FrecuenciaRec(
            cliente_id   = data.cliente_id,
            tipo_id      = tipo_id,
            diasem_mask  = diasem_mask,
            dias_mes     = data.dias_mes,
            hora_desde   = data.hora_desde,
            hora_hasta   = data.hora_hasta,
            veces        = data.veces,
            capacidad_kg = data.capacidad_kg,
            activo       = 1 if (data.activo is None or data.activo) else 0,
            observ       = data.observ,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec
    
    def update(self, frec_id: int, data: FrecuenciaUpdate) -> Optional[FrecuenciaRec]:
        rec = self.db.get(FrecuenciaRec, frec_id)
        if not rec:
            return None

        tipo_id = self._tipo_id(data.tipo_nombre)

        diasem_mask = None
        if data.tipo_nombre in ("diaria", "semanal"):
            dias = data.dias_semana or (list(range(1,8)) if data.tipo_nombre=="diaria" else [])
            diasem_mask = FrecuenciaRec.to_mask(dias)

        rec.tipo_id      = tipo_id
        rec.diasem_mask  = diasem_mask
        rec.dias_mes     = data.dias_mes
        rec.hora_desde   = data.hora_desde
        rec.hora_hasta   = data.hora_hasta
        rec.veces        = data.veces
        rec.capacidad_kg = data.capacidad_kg
        rec.activo       = 1 if (data.activo is None or data.activo) else 0
        rec.observ       = data.observ

        self.db.commit()
        self.db.refresh(rec)
        return rec

    def deactivate(self, frec_id: int) -> None:
        r = self.db.get(FrecuenciaRec, frec_id)
        if not r: return
        r.activo = 0
        self.db.commit()
