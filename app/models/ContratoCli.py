from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class ContratoCli(Base):
    __tablename__ = "contratos_cli"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column("cod_cli", Integer, ForeignKey("clientes.cod_cli"), nullable=False, index=True)

    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    lugar_ejecucion = Column(String(150), nullable=False)

    rep_nombre = Column(String(120), nullable=False)
    rep_cc = Column(String(30), nullable=False)
    rep_exp_lugar = Column(String(80), nullable=False)

    fecha_firma = Column(Date, nullable=False)
    mes_actual = Column(String(20), nullable=False)

    docx_path = Column(String(255), nullable=True)
    pdf_path = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    cliente = relationship("Cliente", back_populates="contratos")