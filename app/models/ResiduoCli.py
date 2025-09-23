from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base


class ResiduosCli(Base):
    __tablename__ = "residuoscli"
    id = Column("cod_residcli", Integer, primary_key=True, index=True)
    codcli = Column("codcli_residcli", Integer, ForeignKey("clientes.cod_cli"))
    tresiduo = Column("codtipores_residcli", Integer,
                      ForeignKey("tiposresid.cod_tipores"))
    cantresiduo = Column("cantidad_residcli", Float)
    pesopromres = Column("pesoprom_residcli", Float)
    segregares = Column("segregacion_residcli", String(50))
    numbolsas = Column("numbolsas_residcli", Integer)
    observaciones = Column("observ_residcli", String(200))
    cliente = relationship("Cliente", back_populates="residuos")
    tipo_residuo = relationship(
        "TipoResiduo", back_populates="residuos_cliente")
