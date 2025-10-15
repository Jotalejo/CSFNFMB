# models/TipoFrecuencia.py
from sqlalchemy import Column, Integer, String
from .base import Base

class TipoFrecuencia(Base):
    __tablename__ = "tiposfrec"
    id = Column("cod_tfrec", Integer, primary_key=True, autoincrement=True)
    nombre = Column("nom_tfrec", String(20), unique=True, nullable=False)
    observaciones = Column("observ_tfrec", String(200))
