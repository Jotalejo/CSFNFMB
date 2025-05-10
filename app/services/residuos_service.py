from sqlalchemy.orm import Session

from models import ResiduosCli
from schemas import ResCliCreate, ResCliClass
from schemas import ResCliClass as ResCliSchema 

# Operaciones en la base de datos para los residuos del cliente
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

#    def get_clientes(self, skip:int=0, limit:int=100):
#        return self.db.query(Cliente).offset(skip).limit(limit).all()
    
    def get_clientes(self, skip:int=0, limit:int=100):
        return (self.db.query(Cliente)
                .order_by(Cliente.razonSocial)  # Ordenamos por la columna
                .offset(skip)
                .limit(limit)
                .all())

    def get_clixlet(self, letra:str=None, skip:int=0, limit:int=100):
        query = self.db.query(Cliente)

        if letra:
            query = query.filter(Cliente.razonSocial.like(f"{letra}%"))

        return (query
                .order_by(Cliente.razonSocial)
                .offset(skip)
                .limit(limit)
                .all())

    def get_cliporID(self, id:int=None, skip:int=0, limit:int=100):
        query = self.db.query(Cliente)

        if id is not None:
            query = query.filter(Cliente.id == id)

        return (query
                .order_by(Cliente.razon_social)
                .offset(skip)
                .limit(limit)
                .all())
    
    

