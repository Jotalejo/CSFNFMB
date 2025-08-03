from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from . import Base

class Citas(Base):
    __tablename__ = "citas"
    id = Column("cod_cita", Integer,primary_key=True,index=True)
    clipot=Column("codclipot_cita", Integer)
    fechacita=Column("fec_cita", Date)
    horacita=Column("hora_cita", Time)
    cliente=Column("codcli_cita", Integer)
    asuntocita=Column("asunto_cita", String(200))
    tipodevisi=Column("codtipovis_cita", Integer)
    iniciocita=Column("inicio_cita", Time)
    fincita=Column("fin_cita", Time)
    actpendcita=Column("actpend_cita", String(200))
    seguiapcita=Column("fecactpen_cita", Date)
    actrealcita=Column("actrealiz_cita", String(200))
    compromcita=Column("compr_cita", String(200))
    fecompromcita=Column("feccompr_cita", Date)
    lugarcita=Column("lugar_cita", String(45))
    ubiccita=Column("ubicac_cita", String(100))
    tipogen=Column("codtipogen_cita", Integer)
    ciudad=Column("ciudad_cita", Integer)
    regioncita=Column("region_cita", String(45))
    observaciones=Column("observ_cita", String(200))
    
