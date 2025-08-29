# models/Citas.py
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Index
from . import Base

class Cita(Base):
    __tablename__ = "citas"

    id            = Column("cod_cita", Integer, primary_key=True, autoincrement=True, index=True)

    # FK opcionales (deja los ForeignKey si ya tienes esas tablas; si no, puedes quitarlos)
    clipot        = Column("codclipot_cita", Integer, ForeignKey("clientespot.cod_clipot"), nullable=True, index=True)
    fechacita     = Column("fec_cita", Date, nullable=True)
    horacita      = Column("hora_cita", Time, nullable=True)
    cliente       = Column("codcli_cita", Integer, ForeignKey("clientes.cod_cli"), nullable=True, index=True)

    asuntocita    = Column("asunto_cita", String(200), nullable=True)
    tipodevisi    = Column("codtipovis_cita", Integer, ForeignKey("tiposvisita.cod_tipovis"), nullable=True, index=True)

    iniciocita    = Column("inicio_cita", Time, nullable=True)
    fincita       = Column("fin_cita", Time, nullable=True)

    actpendcita   = Column("actpend_cita", String(200), nullable=True)
    seguiapcita   = Column("fecactpen_cita", Date, nullable=True)

    actrealcita   = Column("actrealiz_cita", String(200), nullable=True)
    compromcita   = Column("compr_cita", String(200), nullable=True)
    fecompromcita = Column("feccompr_cita", Date, nullable=True)

    lugarcita     = Column("lugar_cita", String(45), nullable=True)
    ubiccita      = Column("ubicac_cita", String(100), nullable=True)

    tipogen       = Column("codtipogen_cita", Integer, ForeignKey("tipogenerador.cod_tipogen"), nullable=True, index=True)

    ciudad        = Column("ciudad_cita", Integer, nullable=True)
    regioncita    = Column("region_cita", String(45), nullable=True)
    observaciones = Column("observ_cita", String(200), nullable=True)

# Índices útiles (opcional)
Index("ix_citas_clipot_fecha", Cita.clipot, Cita.fechacita)
Index("ix_citas_cliente_fecha", Cita.cliente, Cita.fechacita)

    
