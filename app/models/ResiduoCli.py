from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from . import Base

class ResiduosCli(Base):
    __tablename__ = "residuoscli"
    id = Column("cod_residcli", Integer,primary_key=True,index=True)
    ccliente = Column("codcli_residcli", Integer)
    tresiduo = Column("codtipores_residcli", Integer)
    cantresiduo = Column("cantidad_residcli", Float)
    pesopromres = Column("pesoprom_residcli", Float)
    segregares=Column("segregacion_residcli", String(50))
    numbolsas=Column("numbolsas_residcli", Integer)
    observaciones=Column("observ_residcli", String(200))
    