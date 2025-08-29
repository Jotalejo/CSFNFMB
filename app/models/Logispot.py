from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Logispot(Base):
    __tablename__ = "logipot"
    id = Column("cod_logipot", Integer,primary_key=True,index=True)
    codclipot=Column("codclipot_logipot", Integer)
    frecuerec=Column("frecuenciarec_logipot", String(50))
    capavehic=Column("capacvehiculo_logipot", String(100))
    distancia = Column("distancia_logipot", Float)
    observaciones=Column("observ_logipot", String(200))
    