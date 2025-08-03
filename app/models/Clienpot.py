from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Clientespot(Base):
    __tablename__ = "clientespot"
    id = Column("cod_clipot", Integer,primary_key=True,index=True)
    razonSocial=Column("razsoc_clipot", String(100), index=True)
    nit=Column("nit_clipot", String(20))
    direccion=Column("dir_clipot", String(150))
    telefono=Column("tel_clipot", String(50))
    ciudad=Column("ciu_clipot", Integer)
    contacto=Column("contacto_clipot", String(100))
    telefonoContacto=Column("celcontac_clipot", String(50))
    actividad=Column("activ_clipot", String(100))
    email=Column("email_clipot", String(50))
    observaciones=Column("observ_clipot", String(200))
    
