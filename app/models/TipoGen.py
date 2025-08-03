from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class TipoGen(Base):
    __tablename__ = 'tipogenerador'

    id = Column("cod_tipogen", Integer, primary_key=True, autoincrement=True)
    nombre = Column("nom_tipogen", String(45))
    tamax=Column("tamamax_tipogen", Integer)
    tamin=Column("tamamin_tipogen", Integer)
    observaciones = Column("observ_tipogen", String(200))