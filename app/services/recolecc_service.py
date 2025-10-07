# services/recolecc_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

# ✅ Importa SIEMPRE la clase con alias claro
from models.Recoleccion import Recoleccion as RecoleccionModel
from models.Cliente import Cliente as ClienteModel
from models.Estado import Estado as EstadoModel
from models.TipoResiduo import TipoResiduo as TipoResiduoModel

from schemas.Recolecc import RecolectCreate


class RecoleccService:
    def __init__(self, db: Session):
        self.db = db

    # Listado con relaciones cargadas (evita N+1)
    def get_recolecc(self) -> List[RecoleccionModel]:
        return (
            self.db.query(RecoleccionModel)
            .options(
                joinedload(RecoleccionModel.cliente_rel),
                joinedload(RecoleccionModel.estado),
                joinedload(RecoleccionModel.tipo_residuo),
                # joinedload(RecoleccionModel.vehiculo_rel),  # si luego habilitas la relación
            )
            .all()
        )

    def get_recolecc_by_id(self, rec_id: int) -> Optional[RecoleccionModel]:
        # Si usas SQLAlchemy 1.4/2.0, .get está OK; en 1.3 usa query.get(rec_id)
        return self.db.get(RecoleccionModel, rec_id)

    def create_recolecc(self, data: RecolectCreate) -> RecoleccionModel:
        # ❗ NO uses RecoleccionModel.Recoleccion(...) — RecoleccionModel YA es la clase
        rec = RecoleccionModel(
            cliente=data.cliente,
            fecha=data.fecha,
            # hora=data.hora,  # si lo usas
            tresiduo=data.tresiduo,
            cantresiduo=data.cantresiduo,
            peso=data.peso,
            estado_id=data.estado or 1,     # estado inicial = 1
            vehiculo=data.vehiculo,
            codigobar=data.codigobar,
            firmarecolec=data.firmarecolec,
            lafirmaderecibo=data.lafirmaderecibo,
            observaciones=data.observaciones,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def update_recolecc(self, rec_id: int, data: RecolectCreate) -> RecoleccionModel:
        rec = self.get_recolecc_by_id(rec_id)
        if not rec:
            raise ValueError("Recolección no encontrada")

        # Pydantic v2
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rec, field, value)

        self.db.commit()
        self.db.refresh(rec)
        return rec

    def delete_recolecc(self, rec_id: int) -> None:
        rec = self.get_recolecc_by_id(rec_id)
        if not rec:
            return
        self.db.delete(rec)
        self.db.commit()

    # ------- Helpers de clientes -------
    def get_clientes(self, skip: int = 0, limit: int = 100) -> List[ClienteModel]:
        return (
            self.db.query(ClienteModel)
            .order_by(ClienteModel.razonSocial)  # ⚠️ Ajusta al nombre EXACTO del atributo en tu modelo
            .offset(skip).limit(limit).all()
        )

    def get_clixlet(self, letra: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[ClienteModel]:
        q = self.db.query(ClienteModel)
        if letra:
            q = q.filter(ClienteModel.razonSocial.like(f"{letra}%"))
        return q.order_by(ClienteModel.razonSocial).offset(skip).limit(limit).all()

    def get_cliporID(self, id: int) -> Optional[ClienteModel]:
        return self.db.query(ClienteModel).filter(ClienteModel.id == id).first()
