from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Almacenamiento(Base):
    id = Column("cod_almac", Integer, primary_key=True, index=True)
    incinerador_id = Column("codinci_almac", Integer)


# 'cod_almac', 'int', 'NO', 'PRI', NULL, 'auto_increment'
# 'codinci_almac', 'int', 'NO', 'MUL', NULL, ''
# 'pesoalmacenado_almac', 'double', 'YES', '', NULL, ''
# 'fecha_almac', 'date', 'YES', '', NULL, ''
# 'tiempo_almac', 'double', 'YES', '', NULL, ''
# 'responsable_almac', 'varchar(50)', 'YES', '', NULL, ''
# 'observ_almac', 'varchar(200)', 'YES', '', NULL, ''
