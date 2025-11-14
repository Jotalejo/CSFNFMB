# models/Transporte.py
from sqlalchemy import Column, Integer, String, Time, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base

class Transporte(Base):
    __tablename__ = "transporte"

    id            = Column("cod_transp", Integer, primary_key=True, autoincrement=True)
    recoleccion_id= Column("codrecolec_transp", Integer, nullable=True)  # opcional si ya existe recolección
    ruta          = Column("ruta_transp", String(100), nullable=True)
    hora_inicio   = Column("horainicio_transp", Time, nullable=True)
    hora_fin      = Column("horafinal_transp", Time, nullable=True)
    observ        = Column("observ_transp", String(200), nullable=True)
    vehiculo_id   = Column("codvehic_transp", Integer, ForeignKey("vehiculos.cod_vehic"), nullable=False)

# Detalle por parada (recomendado)
class TransporteDetalle(Base):
    __tablename__ = "transporte_detalle"

    id            = Column("cod_transdet", Integer, primary_key=True, autoincrement=True)
    transporte_id = Column(Integer, ForeignKey("codtransp_transdet"), nullable=False)

    # info de la parada
    fecha         = Column("fecha_transdet", Date, nullable=False)
    cliente_id    = Column(Integer, ForeignKey("codcli_transdet"), nullable=False)
    orden         = Column("orden_transdet", Integer, nullable=True)
    direccion     = Column("direccion_transdet", String(200), nullable=True)
    hora_pref     = Column("horapref_transdet", Time, nullable=True)
    ventana_ini   = Column("recolecini_transdet", Time, nullable=True)
    ventana_fin   = Column("recolecfin_transdet", Time, nullable=True)
    capacidad_kg  = Column("capacidad_transdet", Integer, nullable=True)
    lat           = Column("latrecolec_transdet", String(50), nullable=True)  # si manejas coords
    lng           = Column("lngrecolec_transdet", String(50), nullable=True)
    observaciones = Column("observ_transdet", String(200))

    # relaciones si quieres:
    # transporte = relationship("Transporte", backref="detalles")
