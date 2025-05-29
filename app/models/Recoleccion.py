from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Recoleccion(Base):
    __tablename__ = "recoleccion"
    id = Column("cod_recolec", Integer,primary_key=True,index=True)
    cliente=Column("codcli_recolec", Integer)
    fecha=Column("fecha_recolec", Date)
    hora=Column("hora_recolec", Time)
    tresiduo = Column("codtipores_recolec", Integer)
    cantresiduo = Column("cantidbolsas_recolec", Integer)
    peso = Column("pesotot_recolec", Float)
    estado = Column("codest_recolec", Integer)
    vehiculo = Column("codvehic_recolec", Integer)
    codigobar=Column("codigobar_recolec", String(30))
    firmarecolec=Column("firmaentrega_recolec", String(50))
    observaciones=Column("observ_recolec", String(200))