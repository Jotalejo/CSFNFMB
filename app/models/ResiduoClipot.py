from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from . import Base

class ResiduosCli(Base):
    __tablename__ = "residpot"
    id = Column("cod_residpot", Integer,primary_key=True,index=True)
    codcli = Column("codclipot_residpot", Integer)
    tresid = Column("codtipores_residpot", Integer)
    cantresid = Column("cantidad_residpot", Float)
    pesopromres = Column("pesoprom_residpot", Float)
    segregares=Column("segregacion_residpot", String(50))
    numbolsas=Column("numbolsas_residpot", Integer)
    observaciones=Column("observ_residpot", String(200))
    