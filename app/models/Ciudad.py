from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Ciudad(Base):
    __tablename__ = "ciudades"
    id = Column("id", Integer,primary_key=True,index=True)
    codigo=Column("codigo", String(100), index=True)
    nombre=Column("nombre", String(100))
