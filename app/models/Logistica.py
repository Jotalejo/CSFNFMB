from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Logistica(Base):
    __tablename__ = "logistica"

    id = Column("cod_logi", Integer, primary_key=True, autoincrement=True)
    cliente_id = Column("codcli_logi", Integer, nullable=False)  # FK si la tienes
    frecuencia = Column("frecuenciarec_logi", String(50))        # resumen humano
    capacidad_vehiculo = Column("capacvehiculo_logi", Integer)   # si quieres guardar aquí
    distancia = Column("distancia_logi", Float)
    observ = Column("observ_logi", String(200))                  # aquí guardamos JSON (trunca si >200)
