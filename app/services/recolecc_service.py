# services/recolecc_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

# ✅ Importa SIEMPRE la clase con alias claro
from models import Recoleccion, Cliente, TipoResiduo, Estado, DetalleRecoleccion

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
                joinedload(Recoleccion.detalles),
                # joinedload(Recoleccion.vehiculo_rel),  # si luego habilitas la relación
            )
            .all()
        )

    def get_recolecc_by_id(self, rec_id: int) -> Optional[Recoleccion]:
        stmt = select(Recoleccion).where(Recoleccion.id == rec_id).options(
            selectinload(Recoleccion.cliente_rel),
            selectinload(Recoleccion.estado),
            selectinload(Recoleccion.detalles),
            selectinload(Recoleccion.vehiculo_rel)
        )
        result = self.db.execute(stmt).scalars().first()
        return result

    def create_recolecc(self, data: RecolectCreate) -> Recoleccion:
        # ❗ NO uses Recoleccion.Recoleccion(...) — Recoleccion YA es la clase
        # Crea la recolección principal
        # Faltan:

        rec = Recoleccion(
            cliente=data.cliente_id,
            fecha=data.fecha,
            # hora=data.hora,  # si lo usas
            peso=data.peso,
            estado_id=data.estado or 1,     # estado inicial = 1
            tresiduo=data.tresiduo,
            cantresiduo=data.cantresiduo,
            vehiculo=data.vehiculo,
            codigobar=data.codigobar,
            firma_entrega=data.firma_entrega,
            lafirmaderecibo=data.lafirmaderecibo,
            observaciones=data.observaciones,
            # data.ciudad
            # data.contacto
            # data.direccion
            # data.email
            # data.telefono
            # data.telefono_contacto
            # data.firmarecolec
        )
        self.db.add(rec)

        for detalle in data.residuos or []:
            detalle_rec = DetalleRecoleccion(
                recoleccion_id=rec.id,
                tipo_residuo_id=detalle.tresiduo,
                cantidad=detalle.cantidad,
                peso=detalle.peso,
                peso_total=detalle.peso_total,
                fecha=detalle.fecha,
                hora=detalle.hora
            )
            self.db.add(detalle_rec)
        self.db.commit()

    def get_recoleccion_detallada(self, recoleccion_id: int):
        return self.db.query(Recoleccion).join(Recoleccion.cliente_rel).join(Recoleccion.estado).join(Recoleccion.tipo_residuo).where(Recoleccion.id == recoleccion_id).first()

    def create_recolecc(self, recoleccion: RecolectCreate):
        db_recoleccion = Recoleccion(cliente=recoleccion.cliente_id,
                                     fecha=recoleccion.fecha,
                                     hora=recoleccion.hora,
                                     estado_id=recoleccion.estado,
                                     vehiculo=recoleccion.vehiculo,
                                     codigobar=recoleccion.codigobar,
                                     firma_entrega=recoleccion.firmarecolec,
                                     observaciones=recoleccion.observaciones,
                                     lafirmaderecibo=recoleccion.lafirmaderecibo,
                                     email_entrega=recoleccion.email,
                                     telefono_entrega=recoleccion.telefono_contacto,
                                     nombre_entrega=recoleccion.contacto
                                     )
        self.db.add(db_recoleccion)
        self.db.commit()

        for detalle in recoleccion.residuos or []:
            db_detalle = DetalleRecoleccion(
                recoleccion_id=db_recoleccion.id,
                tipo_residuo_id=detalle.tresiduo,
                cantidad=detalle.cantidad,
                peso=detalle.peso,
                peso_total=detalle.peso_total
            )
            self.db.add(db_detalle)
        self.db.commit()
        return recoleccion

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
    def get_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return (
            self.db.query(Cliente)
            # ⚠️ Ajusta al nombre EXACTO del atributo en tu modelo
            .order_by(Cliente.razonSocial)
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

    def get_clixlet(self, letra: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Cliente]:
        q = self.db.query(Cliente)
        if letra:
            q = q.filter(Cliente.razonSocial.like(f"{letra}%"))
        return q.order_by(Cliente.razonSocial).offset(skip).limit(limit).all()

    def get_cliporID(self, id: int) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id == id).first()
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
