from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column("cod_vehic", Integer, primary_key=True, index=True)
    placa = Column("placa_vehic", String(10), unique=True, nullable=False)
    estado = Column("estado_vehic", String(100), nullable=False)
    capacidad = Column("capac_vehic", Integer, nullable=False)
    observaciones = Column("observ_vehic", String(200), nullable=True)
    conductor_id = Column("codpers_vehic", Integer, ForeignKey("persona.cod_pers"), nullable=False)

    # Debe coincidir con back_populates en Recoleccion
    recolecciones = relationship("Recoleccion", back_populates="vehiculo_rel")
    
