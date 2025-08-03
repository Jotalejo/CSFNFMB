from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class TipoVisita(Base):
    __tablename__ = 'tiposvisita'

    id = Column("cod_tipovis", Integer, primary_key=True, autoincrement=True)
    nombre = Column("nom_tipovis", String(45))
    observaciones = Column("observ_tipovis", String(200))