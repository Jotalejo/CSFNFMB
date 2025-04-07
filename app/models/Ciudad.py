from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Ciudad(Base):
    __tablename__ = "ciudades"
    id = Column("cod_ciud", Integer,primary_key=True,index=True)
    nombre=Column("nom_ciud", String(100))
    codigo=Column("codinterno_ciud", Integer, index=True)
    