from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, TIMESTAMP, text
from sqlalchemy.orm import relationship

from .base import Base


class Pesaje(Base):
    __tablename__ = "pesaje"

    id = Column("cod_pesaje", Integer, primary_key=True, index=True, autoincrement=True)

    recoleccion_id = Column(
        "codrecolec_pesaje",
        Integer,
        ForeignKey("recoleccion.cod_recolec"),
        nullable=True
    )

    vehiculo_id = Column(
        "codvehic_pesaje",
        Integer,
        ForeignKey("vehiculos.cod_vehic"),
        nullable=True
    )

    cliente_id = Column(
        "codcli_pesaje",
        Integer,
        ForeignKey("clientes.cod_cli"),
        nullable=True
    )

    created_at = Column(
        "created_at_pesaje",
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    estado = Column("estado_pesaje", String(20), nullable=True)
    fecha = Column("fecha_pesaje", Date, nullable=True)
    firma_verificacion = Column("firmaverific_pesaje", String(50), nullable=True)
    observaciones = Column("observ_pesaje", String(200), nullable=True)

    # Relaciones
    recoleccion = relationship("Recoleccion")
    vehiculo = relationship("Vehiculo")
    cliente = relationship("Cliente")

    detalles = relationship(
        "DetallePesaje",
        back_populates="pesaje",
        cascade="all, delete-orphan"
    )


class DetallePesaje(Base):
    __tablename__ = "detalle_pesaje"

    id = Column(
        "coddetpesaje_detpes",
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    pesaje_id = Column(
        "codpesaje_detpes",
        Integer,
        ForeignKey("pesaje.cod_pesaje"),
        nullable=True
    )

    detalle_recoleccion_id = Column(
        "cod_detrec_detpes",
        Integer,
        ForeignKey("detalle_recoleccion.cod_detrec"),
        nullable=True
    )

    tipo_residuo_id = Column(
        "cod_tipores_detpes",
        Integer,
        ForeignKey("tiposresid.cod_tipores"),
        nullable=True
    )

    bolsas = Column("bolsas_manif_detpes", Integer, nullable=True)
    peso = Column("peso_manif_detpes", Float, nullable=True)
    confirmado = Column("confirmado_detpes", Integer, nullable=True, default=0)
    observaciones = Column("observ_detpes", String(300), nullable=True)

    # Relaciones
    pesaje = relationship("Pesaje", back_populates="detalles")
    detalle_recoleccion = relationship("DetalleRecoleccion")
    tipo_residuo = relationship("TipoResiduo")