from sqlalchemy.orm import Session					
from models import ResiduosCli					
from schemas import ResiduosCliCreate, ResiduosCliUpdate					
					
class ResiduosCliService:					
    def __init__(self, db: Session):					
        self.db = db					
					
    def create_residuo(self, residuo: ResiduosCliCreate):					
        db_residuo = ResiduosCli(**residuo.dict())					
        self.db.add(db_residuo)					
        self.db.commit()					
        self.db.refresh(db_residuo)					
        return db_residuo					
					
    def get_residuos_by_cliente(self, cliente_id: int):					
        return self.db.query(ResiduosCli).filter(ResiduosCli.ccliente == cliente_id).all()					
					
    def update_residuo(self, residuo: ResiduosCliUpdate):					
        db_residuo = self.db.query(ResiduosCli).filter(ResiduosCli.id == residuo.id).first()					
        if db_residuo:					
            for key, value in residuo.dict().items():					
                setattr(db_residuo, key, value)					
            self.db.commit()					
            self.db.refresh(db_residuo)					
        return db_residuo					
					
    def delete_residuo(self, residuo_id: int):					
        db_residuo = self.db.query(ResiduosCli).filter(ResiduosCli.id == residuo_id).first()					
        if db_residuo:					
            self.db.delete(db_residuo)					
            self.db.commit()					
        return db_residuo					
