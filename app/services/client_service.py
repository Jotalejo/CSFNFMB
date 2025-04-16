from sqlalchemy.orm import Session

from models import Cliente
from schemas import ClienteCreate
from schemas import Cliente as ClienteSchema 

class ClienteService:
    def __init__(self, db: Session):
        self.db = db

    def get_cliente(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_cliente_by_nit(self, nit: str):
        return self.db.query(Cliente).filter(Cliente.nit == nit).first()

    def create_cliente(self, cliente: ClienteCreate):
        db_cliente = Cliente(razonSocial=cliente.razonSocial,
                            nit=cliente.nit,
                            direccion=cliente.direccion,
                            telefono=cliente.telefono,
                            ciudad=cliente.ciudad,    
                            contacto=cliente.contacto,
                            telefonoContacto=cliente.telefonoContacto,
                            observaciones=cliente.observaciones,
                            email=cliente.email
                            )
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, cliente:ClienteSchema):
        db_cliente = self.get_cliente(cliente.id)
        db_cliente.razonSocial = cliente.razonSocial
        db_cliente.nit = cliente.nit
        db_cliente.direccion=cliente.direccion,
        db_cliente.telefono=cliente.telefono,
        db_cliente.ciudad=cliente.ciudad,    
        db_cliente.contacto=cliente.contacto,
        db_cliente.telefonoContacto=cliente.telefonoContacto,
        db_cliente.observaciones=cliente.observaciones,
        db_cliente.email=cliente.email
        
        self.db.commit()
        return db_cliente

    def get_clientes(self, skip:int=0, limit:int=100):
        return self.db.query(Cliente).offset(skip).limit(limit).all()
    

