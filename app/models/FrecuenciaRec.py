# models/FrecuenciaRec.py
from sqlalchemy import Column, Integer, String, Time, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from .base import Base

class FrecuenciaRec(Base):
    __tablename__ = "frecuenciarec"
    id = Column("cod_frecrec", Integer, primary_key=True, autoincrement=True)

    cliente_id = Column("codcli_frecrec", Integer, ForeignKey("clientes.cod_cli"), nullable=False)
    tipo_id    = Column("codtfrec_frecrec", Integer, ForeignKey("tiposfrec.cod_tfrec"), nullable=False)

    # 0..127 (L=1, M=2, X=4, J=8, V=16, S=32, D=64)
    diasem_mask = Column("diasem_mask_frecrec", SmallInteger, nullable=True)
    dias_mes    = Column("diasmes_frecrec", String(100), nullable=True)  # "1,10,20,30"

    hora_desde  = Column("horadesde", Time, nullable=True)
    hora_hasta  = Column("horahasta", Time, nullable=True)

    veces       = Column("veces_frecrec", Integer, nullable=True)
    capacidad_kg= Column("capacest_frecrec", Integer, nullable=True)
    activo      = Column("activo_frecrec", SmallInteger, nullable=False, default=1)
    observ      = Column("observ_frecrec", String(200), nullable=True)

    tipo = relationship("TipoFrecuencia")
    # si tienes Cliente model:
    # cliente = relationship("Cliente", back_populates="frecuencias")

    # Helpers (no se mapean a DB):
    @staticmethod
    def to_mask(dias: list[int]) -> int:
        # dias: 1=Lunes..7=Domingo
        bits = [1,2,4,8,16,32,64]
        mask = 0
        for d in dias or []:
            if 1 <= d <= 7:
                mask |= bits[d-1]
        return mask

    @staticmethod
    def from_mask(mask: int) -> list[int]:
        bits = [1,2,4,8,16,32,64]
        out = []
        for i,b in enumerate(bits, start=1):
            if mask & b:
                out.append(i)
        return out
