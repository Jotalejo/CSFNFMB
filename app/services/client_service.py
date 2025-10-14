from typing import Optional, List
from sqlalchemy.orm import Session
from models import Cliente as ClienteModel
from schemas import ClienteCreate
from schemas import Cliente as ClienteSchema

class ClienteService:
    def __init__(self, db: Session):
        self.db = db

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
        )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, cliente: ClienteSchema) -> ClienteModel:
        db_cliente = self.get_cliente(cliente.id)
        if not db_cliente:
            return None  # o lanza una excepción si prefieres

        # OJO: quité las comas al final de línea (creaban tuplas y no asignaban)
        db_cliente.razonSocial       = cliente.razonSocial
        db_cliente.nit               = cliente.nit
        db_cliente.direccion         = cliente.direccion
        db_cliente.telefono          = cliente.telefono
        db_cliente.ciudad            = cliente.ciudad
        db_cliente.contacto          = cliente.contacto
        db_cliente.telefonoContacto  = cliente.telefonoContacto
        db_cliente.observaciones     = cliente.observaciones
        db_cliente.email             = cliente.email

        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    # -------- LISTADOS --------
    # Sin límites por defecto: devuelve TODOS
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
