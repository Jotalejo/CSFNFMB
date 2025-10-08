# services/recolecc_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

# ✅ Importa SIEMPRE la clase con alias claro
from models import Recoleccion
from models.Cliente import Cliente as ClienteModel
from models.Estado import Estado as EstadoModel
from models.TipoResiduo import TipoResiduo as TipoResiduoModel

from schemas.Recolecc import RecolectCreate, Recolecc


# Operaciones en la base de datos para la Recolección


class RecoleccService:
    def __init__(self, db: Session):
        self.db = db

    # Listado con relaciones cargadas (evita N+1)
    def get_recolecc(self) -> List[Recoleccion]:
        return (
            self.db.query(Recoleccion)
            .options(
                joinedload(Recoleccion.cliente_rel),
                joinedload(Recoleccion.estado),
                joinedload(Recoleccion.tipo_residuo),
                # joinedload(Recoleccion.vehiculo_rel),  # si luego habilitas la relación
            )
            .all()
        )

    def get_recolecc_by_id(self, rec_id: int) -> Optional[Recoleccion]:
        # Si usas SQLAlchemy 1.4/2.0, .get está OK; en 1.3 usa query.get(rec_id)
        return self.db.get(Recoleccion, rec_id)

    def create_recolecc(self, data: RecolectCreate) -> Recoleccion:
        # ❗ NO uses Recoleccion.Recoleccion(...) — Recoleccion YA es la clase
        rec = Recoleccion(
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

    def get_recoleccion_detallada(self, recoleccion_id: int):
        return self.db.query(Recoleccion).join(Recoleccion.cliente_rel).join(Recoleccion.estado).join(Recoleccion.tipo_residuo).where(Recoleccion.id == recoleccion_id).first()

    def create_recolecc(self, recoleccion: RecolectCreate):
        db_recoleccion = Recoleccion(cliente=recoleccion.cliente,
                                     fecha=recoleccion.fecha,
                                     hora=recoleccion.hora,
                                     tiporesiduo=recoleccion.tiporesiduo,
                                     cantibolsas=recoleccion.cantibolsas,
                                     pesotot=recoleccion.pesotot,
                                     estado=recoleccion.estado,
                                     vehiculo=recoleccion.vehiculo,
                                     barras=recoleccion.barras,
                                     firmaentrega=recoleccion.firmaentrega,
                                     observaciones=recoleccion.observaciones
                                     )
        self.db.add(db_recoleccion)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def update_recolecc(self, rec_id: int, data: RecolectCreate) -> Recoleccion:
        rec = self.get_recolecc_by_id(rec_id)
        if not rec:
            raise ValueError("Recolección no encontrada")

        # Pydantic v2
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rec, field, value)

    def update_recolecc(self, recoleccion: Recoleccion):
        db_recoleccion = self.get_recolecc(recoleccion.id)
        db_recoleccion.cliente = recoleccion.cliente
        db_recoleccion.fecha = recoleccion.fecha
        db_recoleccion.hora = recoleccion.hora,
        db_recoleccion.tiporesiduo = recoleccion.tiporesiduo,
        db_recoleccion.cantibolsas = recoleccion.cantibolsas,
        db_recoleccion.pesotot = recoleccion.pesotot,
        db_recoleccion.estado = recoleccion.estado,
        db_recoleccion.vehiculo = recoleccion.vehiculo,
        db_recoleccion.firmaentrega = recoleccion.firmaentrega,
        db_recoleccion.observaciones = recoleccion.observaciones
        self.db.commit()
        self.db.refresh(recoleccion)
        return recoleccion

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
            # ⚠️ Ajusta al nombre EXACTO del atributo en tu modelo
            .order_by(ClienteModel.razonSocial)
            .offset(skip).limit(limit).all()
        )
#    def get_clientes(self, skip:int=0, limit:int=100):
#        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def get_clientes(self, skip: int = 0, limit: int = 100):
        return (self.db.query(Cliente)
                .order_by(Cliente.razonSocial)  # Ordenamos por la columna
                .offset(skip)
                .limit(limit)
                .all())

    def get_clixlet(self, letra: str = None, skip: int = 0, limit: int = 100):
        query = self.db.query(Cliente)

    def get_clixlet(self, letra: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[ClienteModel]:
        q = self.db.query(ClienteModel)
        if letra:
            q = q.filter(ClienteModel.razonSocial.like(f"{letra}%"))
        return q.order_by(ClienteModel.razonSocial).offset(skip).limit(limit).all()

    def get_cliporID(self, id: int) -> Optional[ClienteModel]:
        return self.db.query(ClienteModel).filter(ClienteModel.id == id).first()
        return (query
                .order_by(Cliente.razonSocial)
                .offset(skip)
                .limit(limit)
                .all())

    def get_cliporID(self, id: int = None, skip: int = 0, limit: int = 100):
        query = self.db.query(Cliente)

        if id is not None:
            query = query.filter(Cliente.id == id)

        return (query
                .order_by(Cliente.razon_social)
                .offset(skip)
                .limit(limit)
                .all())

# Residusos del Cliente  :
# Operaciones en la base de datos para el Residuo del cliente :

# Operaciones en la base de datos para el cliente
