# models/Residuoclipot.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from .base import Base


class ResiduosClientePotencial(Base):
    __tablename__ = "residpot"

    id = Column("cod_residpot", Integer, primary_key=True,
                autoincrement=True, index=True)
    ccliente = Column("codclipot_residpot", Integer, ForeignKey(
        "clientespot.cod_clipot"), index=True, nullable=True)
    tresiduo = Column("codtipores_residpot", Integer,
                      index=True, nullable=True)
    cantresiduo = Column("cantidad_residpot", Float, nullable=True)
    pesopromres = Column("pesoprom_residpot", Float, nullable=True)
    segregares = Column("segregacion_residpot", String(50), nullable=True)
    numbolsas = Column("numbolsas_residpot", Integer, nullable=True)
    observaciones = Column("observ_residpot", String(200), nullable=True)


# Índices útiles
Index("ix_residpot_clipot", ResiduosClientePotencial.ccliente)
Index("ix_residpot_tipores", ResiduosClientePotencial.tresiduo)
