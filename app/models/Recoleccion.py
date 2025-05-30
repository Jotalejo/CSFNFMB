from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float
from sqlalchemy.orm import relationship
from . import Base

class Recoleccion(Base):
    __tablename__ = "recoleccion"
    id = Column("cod_recolec", Integer,primary_key=True,index=True)
    cliente=Column("codcli_recolec", Integer, ForeignKey("clientes.cod_cli"))
    tresiduo = Column("codtipores_recolec", Integer, ForeignKey("tiposresid.cod_tipores"))
    estado_id = Column("codest_recolec", Integer, ForeignKey("estados.cod_est"))
    fecha=Column("fecha_recolec", Date)
    hora=Column("hora_recolec", Time)
    cantresiduo = Column("cantidbolsas_recolec", Integer)
    peso = Column("pesotot_recolec", Float)
    vehiculo = Column("codvehic_recolec", Integer)
    codigobar=Column("codigobar_recolec", String(30))
    firmarecolec=Column("firmaentrega_recolec", String(50))
    observaciones=Column("observ_recolec", String(200))
    cliente_rel = relationship("Cliente", back_populates="recolecciones")
    estado = relationship("Estado", back_populates="recolecciones")
    tipo_residuo = relationship("TipoResiduo", back_populates="recolecciones")