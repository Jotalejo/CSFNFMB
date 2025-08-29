# models/Clienpot.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from . import Base

class Clientespot(Base):
    __tablename__ = "clientespot"

    id = Column("cod_clipot", Integer, primary_key=True, index=True, autoincrement=True)
    razonSocial = Column("razsoc_clipot", String(100), unique=True, index=True)   # UNI
    nit         = Column("nit_clipot", String(20), unique=True, index=True)       # UNI
    direccion   = Column("dir_clipot", String(150))
    telefono    = Column("tel_clipot", String(50))
    ciudad      = Column("ciu_clipot", Integer)
    contacto           = Column("contacto_clipot", String(100))
    telefonoContacto   = Column("celcontac_clipot", String(50))
    actividad    = Column("activ_clipot", String(100))
    email        = Column("email_clipot", String(50))
    observaciones= Column("observ_clipot", String(200))

    __table_args__ = (
        UniqueConstraint("razsoc_clipot", name="uq_clientespot_razsoc"),
        UniqueConstraint("nit_clipot", name="uq_clientespot_nit"),
    )