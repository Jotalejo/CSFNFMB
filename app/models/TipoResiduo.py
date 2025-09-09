from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class TipoResiduo(Base):
    __tablename__ = 'tiposresid'

    id = Column("cod_tipores", Integer, primary_key=True, autoincrement=True)
    nombre = Column("nomtipo_tipores", String(45), unique=True, nullable=True)
    clasificacion = Column("codsubclres_tipores", Integer, nullable=True)
    observaciones = Column("observ_tipores", String(200), nullable=True)
    
    recolecciones = relationship("Recoleccion", back_populates="tipo_residuo")

