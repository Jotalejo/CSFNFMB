from sqlalchemy.orm import Session

from models import Ciudad
from schemas import ClienteCreate
from schemas import Cliente as ClienteSchema 

class CiudadService:
    def __init__(self, db: Session):
        self.db = db

    def get_ciudades(self, skip:int=0, limit:int=200):
        return self.db.query(Ciudad).offset(skip).limit(limit).all()

