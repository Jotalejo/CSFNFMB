# models/Logispot.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from . import Base

class Logispot(Base):
    __tablename__ = "logipot"

    id          = Column("cod_logipot", Integer, primary_key=True, autoincrement=True, index=True)
    codclipot   = Column("codclipot_logipot", Integer, ForeignKey("clientespot.cod_clipot"), index=True, nullable=True)
    frecuerec   = Column("frecuenciarec_logipot", String(50), nullable=True)
    capavehic   = Column("capacvehiculo_logipot", String(100), nullable=True)
    distancia   = Column("distancia_logipot", Float, nullable=True)
    observaciones = Column("observ_logipot", String(200), nullable=True)

# Índice útil
Index("ix_logipot_clipot", Logispot.codclipot)
