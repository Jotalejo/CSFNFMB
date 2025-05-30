from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Estado(Base):
    __tablename__ = "estados"
    id = Column("cod_est", Integer, primary_key=True, index=True)
    nombre = Column("nom_est", String(100), index=True)
    clase = Column("clase_est", String(50), index=True)
    observaciones = Column("observ_est", String(200))
    recolecciones = relationship("Recoleccion", back_populates="estado")
