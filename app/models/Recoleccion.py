from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float
from sqlalchemy.orm import relationship
from .base import Base


class Recoleccion(Base):
    __tablename__ = "recoleccion"

    id = Column("cod_recolec", Integer, primary_key=True,
                index=True, autoincrement=True)

    # FKs
    cliente = Column("codcli_recolec", Integer, ForeignKey("clientes.cod_cli"))
    tresiduo = Column("codtipores_recolec", Integer,
                      ForeignKey("tiposresid.cod_tipores"))
    estado_id = Column("codest_recolec", Integer,
                       ForeignKey("estados.cod_est"))
    vehiculo = Column("codvehic_recolec", Integer, ForeignKey(
        "vehiculos.cod_vehic"), nullable=True)

    # Datos de la recolección
    fecha = Column("fecha_recolec", Date)
    hora = Column("hora_recolec", Time)
    cantresiduo = Column("cantidbolsas_recolec", Integer)
    peso = Column("pesotot_recolec", Float)
    codigobar = Column("codigobar_recolec", String(30))
    firmarecolec = Column("firmaentrega_recolec", String(50))
    lafirmaderecibo = Column("lafirmaderecibo_recolec", String(
        50), nullable=True)  # ⬅️ nuevo campo
    observaciones = Column("observ_recolec", String(200))

    # Relaciones
    cliente_rel = relationship("Cliente", back_populates="recolecciones")
    tipo_residuo = relationship("TipoResiduo", back_populates="recolecciones")
    estado = relationship("Estado", back_populates="recolecciones")
    vehiculo_rel = relationship("Vehiculo", back_populates="recolecciones")
