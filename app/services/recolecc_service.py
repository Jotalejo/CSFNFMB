from sqlalchemy.orm import Session
from models import Recoleccion
from schemas import RecolectCreate
from schemas import Recolecc as RecoleccSchema

# Operaciones en la base de datos para la Recolección
class RecoleccService:
    def __init__(self, db: Session):
        self.db = db

    def get_recolecc(self):
        return self.db.query(Recoleccion).join(Recoleccion.cliente_rel).join(Recoleccion.estado).join(Recoleccion.tipo_residuo).all()

    def create_recolecc(self, recoleccion: RecolectCreate):
        db_recoleccion = Recoleccion(cliente=recoleccion.cliente,
                            fecha=recoleccion.fecha,
                            hora=recoleccion.hora,
                            tiporesiduo=recoleccion.tiporesiduo,
                            cantibolsas=recoleccion.cantibolsas,    
                            pesotot=recoleccion.pesotot,
                            estado=recoleccion.estado,
                            vehiculo=recoleccion.vehiculo,
                            barras=recoleccion.barras,
                            firmaentrega=recoleccion.firmaentrega,
                            observaciones=recoleccion.observaciones
                            )
        self.db.add(db_recoleccion)
        self.db.commit()
        self.db.refresh(db_recoleccion)
        return db_recoleccion

    def update_recolecc(self, recolecc:RecoleccSchema):
        db_recoleccion = self.get_recolecc(recoleccion.id)
        db_recoleccion.cliente = recoleccion.cliente
        db_recoleccion.fecha = recoleccion.fecha
        db_recoleccion.hora=recoleccion.hora,
        db_recoleccion.tiporesiduo=recoleccion.tiporesiduo,
        db_recoleccion.cantibolsas=recoleccion.cantibolsas,    
        db_recoleccion.pesotot=recoleccion.pesotot,
        db_recoleccion.estado=recoleccion.estado,
        db_recoleccion.vehiculo=recoleccion.vehiculo,
        db_recoleccion.firmaentrega=recoleccion.firmaentrega,
        db_recoleccion.observaciones=recoleccion.observaciones
        self.db.commit()
        return db_cliente

#    def get_clientes(self, skip:int=0, limit:int=100):
#        return self.db.query(Cliente).offset(skip).limit(limit).all()
    
    def get_clientes(self, skip:int=0, limit:int=100):
        return (self.db.query(Cliente)
                .order_by(Cliente.razonSocial)  # Ordenamos por la columna
                .offset(skip)
                .limit(limit)
                .all())

    def get_clixlet(self, letra:str=None, skip:int=0, limit:int=100):
        query = self.db.query(Cliente)

        if letra:
            query = query.filter(Cliente.razonSocial.like(f"{letra}%"))

        return (query
                .order_by(Cliente.razonSocial)
                .offset(skip)
                .limit(limit)
                .all())

    def get_cliporID(self, id:int=None, skip:int=0, limit:int=100):
        query = self.db.query(Cliente)

        if id is not None:
            query = query.filter(Cliente.id == id)

        return (query
                .order_by(Cliente.razon_social)
                .offset(skip)
                .limit(limit)
                .all())
    
#######  Residusos del Cliente  :
# Operaciones en la base de datos para el Residuo del cliente :
    
# Operaciones en la base de datos para el cliente
