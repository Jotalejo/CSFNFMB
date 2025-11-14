# services/client_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Cliente as ClienteModel
from schemas import ClienteCreate
from schemas import Cliente as ClienteSchema

from fastapi import HTTPException

class ClienteService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Helpers ----------

    @staticmethod
    def generar_linkmaps(lat: Optional[float], lng: Optional[float]) -> Optional[str]:
        if lat is None or lng is None:
            return None
        return f"https://www.google.com/maps?q={lat},{lng}"

    # ---------- CRUD ----------

    def get_cliente(self, cliente_id: int) -> Optional[ClienteModel]:
        return (
            self.db.query(ClienteModel)
            .filter(ClienteModel.id == cliente_id)
            .first()
        )

    def get_cliente_by_nit(self, nit: str) -> Optional[ClienteModel]:
        return (
            self.db.query(ClienteModel)
            .filter(ClienteModel.nit == nit)
            .first()
        )

    def create_cliente(self, cliente: ClienteCreate) -> ClienteModel:
        # si no viene linkmaps pero sí lat/lng, lo generamos
        linkmaps = cliente.linkmaps
        if not linkmaps and cliente.latrecolec is not None and cliente.lngrecolec is not None:
            linkmaps = self.generar_linkmaps(cliente.latrecolec, cliente.lngrecolec)

        db_cliente = ClienteModel(
            razonSocial=cliente.razonSocial,
            nit=cliente.nit,
            direccion=cliente.direccion,
            telefono=cliente.telefono,
            ciudad=cliente.ciudad,
            contacto=cliente.contacto,
            telefonoContacto=cliente.telefonoContacto,
            observaciones=cliente.observaciones,
            email=cliente.email,
            # nuevos campos
            latrecolec=cliente.latrecolec,
            lngrecolec=cliente.lngrecolec,
            linkmaps=linkmaps,
        )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, cliente: ClienteSchema) -> Optional[ClienteModel]:
        db_cliente = self.get_cliente(cliente.id)
        if not db_cliente:
            return None

        db_cliente.razonSocial       = cliente.razonSocial
        db_cliente.nit               = cliente.nit
        db_cliente.direccion         = cliente.direccion
        db_cliente.telefono          = cliente.telefono
        db_cliente.ciudad            = cliente.ciudad
        db_cliente.contacto          = cliente.contacto
        db_cliente.telefonoContacto  = cliente.telefonoContacto
        db_cliente.observaciones     = cliente.observaciones
        db_cliente.email             = cliente.email

        # actualizamos lat/lng
        db_cliente.latrecolec        = cliente.latrecolec
        db_cliente.lngrecolec        = cliente.lngrecolec
        db_cliente.linkmaps          = cliente.linkmaps or db_cliente.linkmaps

        # si viene linkmaps desde el front, úsalo; si no, lo generamos si hay coords
        # if cliente.linkmaps:
        #    db_cliente.linkmaps = cliente.linkmaps
        # else:
        #    if cliente.latrecolec is not None and cliente.lngrecolec is not None:
        #        db_cliente.linkmaps = self.generar_linkmaps(
        #            cliente.latrecolec, cliente.lngrecolec
        #        )

        if not db_cliente.linkmaps and db_cliente.latrecolec is not None and db_cliente.lngrecolec is not None:
            db_cliente.linkmaps = self.generar_linkmaps(db_cliente.latrecolec, db_cliente.lngrecolec)

        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    # -------- LISTADOS --------

    def get_clientes(
        self,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[ClienteModel]:
        q = self.db.query(ClienteModel).order_by(ClienteModel.razonSocial)
        if skip is not None and skip > 0:
            q = q.offset(skip)
        if limit is not None and limit > 0:
            q = q.limit(limit)
        return q.all()

    def get_clixlet(
        self,
        letra: Optional[str] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[ClienteModel]:
        q = self.db.query(ClienteModel)
        if letra:
            q = q.filter(ClienteModel.razonSocial.like(f"{letra}%"))
        q = q.order_by(ClienteModel.razonSocial)
        if skip is not None and skip > 0:
            q = q.offset(skip)
        if limit is not None and limit > 0:
            q = q.limit(limit)
        return q.all()

    def get_cliporID(self, id: int) -> Optional[ClienteModel]:
        return (
            self.db.query(ClienteModel)
            .filter(ClienteModel.id == id)
            .first()
        )
    
    def refresh_linkmaps(self, cliente_id: int) -> ClienteModel:
        db_cliente = self.get_cliente(cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        if db_cliente.latrecolec is None or db_cliente.lngrecolec is None:
            raise HTTPException(
                status_code=400,
                detail="Cliente no tiene lat/lng; no se puede generar linkmaps"
            )

        db_cliente.linkmaps = self.generar_linkmaps(db_cliente.latrecolec, db_cliente.lngrecolec)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def backfill_linkmaps(self) -> int:
        """
        Genera linkmaps para todos los clientes que NO lo tengan,
        pero SÍ tengan lat/lng. Devuelve cuántos actualizó.
        """
        q = (
            self.db.query(ClienteModel)
            .filter(ClienteModel.linkmaps.is_(None))
            .filter(ClienteModel.latrecolec.isnot(None))
            .filter(ClienteModel.lngrecolec.isnot(None))
        )
        count = 0
        for c in q.all():
            c.linkmaps = self.generar_linkmaps(c.latrecolec, c.lngrecolec)
            count += 1
        if count:
            self.db.commit()
        return count
