from sqlalchemy.orm import Session

import api.models as models
import api.schemas as schemas


def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def get_cliente_by_nit(db: Session, nit: str):
    return db.query(models.Cliente).filter(models.Cliente.nit == nit).first()

def create_client(db: Session, cliente:schemas.ClienteCreate):
    db_cliente = models.Cliente.User(razonSocial=cliente.razonSocial,
                          nit=cliente.razonSocial)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

