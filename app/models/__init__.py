from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .Cliente import Cliente
from .Ciudad import Ciudad
from .ResiduoCli import ResiduosCli
from .Recoleccion import Recoleccion
from .Estado import Estado
from .TipoResiduo import TipoResiduo
from .Vehiculo import Vehiculo
