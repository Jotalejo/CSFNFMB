from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Residuos(Base):
    __tablename__ = "residuos"
    id = Column("cod_resid", Integer,primary_key=True,index=True)
    tipoResiduo=Column("codtipores_residuo", Integer, ForeignKey("tiporesiduos.cod_tiporesid"), index=True)
    nombreResiduo=Column("nombre_resid", String(50), index=True)
    disposicResiduo=Column("disposic_residuo", String(50))
    observResiduo=Column("observ_residuo", String(200))
    
    # tipoResiduo = relationship("TipoResiduo", back_populates="residuos")
    # tipoResiduo = relationship("TipoResiduo", backref="residuos")
    