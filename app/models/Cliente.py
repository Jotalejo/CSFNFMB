from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column("cod_cli", Integer, primary_key=True, index=True)
    razonSocial = Column("razonsoc_cli", String(100), index=True)
    nit = Column("nit_cli", String(20))
    direccion = Column("direc_cli", String(150))
    telefono = Column("telef_cli", String(50))
    ciudad = Column("ciudad_cli", Integer)
    actividad = Column("actividad_cli", String(100))
    email = Column("email_cli", String(50))
    contacto = Column("contacto_cli", String(50))
    telefonoContacto = Column("telcont_cli", String(15))
    estadocarta = Column("estadocartera_cli", Integer)
    observaciones = Column("observ_cli", String(200))
    recolecciones = relationship("Recoleccion", back_populates="cliente_rel")
    residuos = relationship("ResiduosCli", back_populates="cliente")
