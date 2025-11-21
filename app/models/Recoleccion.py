from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float
from sqlalchemy.orm import relationship
from .base import Base


# cod_recolec
# codcli_recolec
# fecha_recolec
# hora_recolec
# codtipores_recolec
# cantidbolsas_recolec
# pesotot_recolec
# codest_recolec
# codvehic_recolec
# codigobar_recolec
# firmaentrega_recolec
# lafirmaderecibo_recolec
# observ_recolec

class Recoleccion(Base):
    __tablename__ = "recoleccion"

    id = Column("cod_recolec", Integer, primary_key=True,
                index=True, autoincrement=True)

    # FKs
    cliente = Column("codcli_recolec", Integer, ForeignKey("clientes.cod_cli"))
    estado_id = Column("codest_recolec", Integer,
                       ForeignKey("estados.cod_est"))
    vehiculo = Column("codvehic_recolec", Integer, ForeignKey(
        "vehiculos.cod_vehic"), nullable=True)

    # Datos de la recolección
    fecha = Column("fecha_recolec", Date)
    hora = Column("hora_recolec", Time)

    # cantresiduo = Column("cantidbolsas_recolec", Integer)
    # peso = Column("pesotot_recolec", Float)
    codigobar = Column("codigobar_recolec", String(30))

    firma_entrega = Column("firmaentrega_recolec", String(50))
    lafirmaderecibo = Column("lafirmaderecibo_recolec", String(
        50), nullable=True)  # ⬅️ nuevo campo
    observaciones = Column("observ_recolec", String(200))

    nombre_entrega = Column("nombre_qentrega_recolec", String(100), nullable=True)  # ⬅️ nuevo campo
    email_entrega = Column("email_qentrega_recolec", String(50), nullable=True)  # ⬅️ nuevo campo
    telefono_entrega = Column("cel_qentrega_recolec", String(15), nullable=True)  # ⬅️ nuevo campo

    # Relaciones
    cliente_rel = relationship("Cliente", back_populates="recolecciones")
    # tresiduo = Column("codtipores_recolec", Integer,                       ForeignKey("tiposresid.cod_tipores"))
    # tipo_residuo = relationship("TipoResiduo", back_populates="recolecciones")
    estado = relationship("Estado", back_populates="recolecciones")
    vehiculo_rel = relationship("Vehiculo", back_populates="recolecciones")
    detalles = relationship(
        "DetalleRecoleccion", back_populates="recoleccion", cascade="all, delete-orphan")


class DetalleRecoleccion(Base):
    __tablename__ = "detalle_recoleccion"

    id = Column("cod_detrec", Integer, primary_key=True,
                index=True, autoincrement=True)

    recoleccion_id = Column("codrecolec_detrec", Integer,
                            ForeignKey("recoleccion.cod_recolec"))
    tipo_residuo_id = Column("codtipores_detrec", Integer,
                             ForeignKey("tiposresid.cod_tipores"))
    cantidad = Column("cantidbolsas_detrec", Integer)
    peso = Column("peso_detrec", Float)
    peso_total = Column("pesotot_detrec", Float)
    codigo_barras = Column("codigobar_detrec", String(45))
    observaciones = Column("observ_detrec", String(200))

    # Relaciones
    tipo_residuo = relationship("TipoResiduo")
    recoleccion = relationship("Recoleccion", back_populates="detalles")
    # Recoleccion.detalles = relationship("Detalle", back_populates="recoleccion")
