# services/residuoscli.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import ResiduosCli as ResidModel

class ResiduosCliService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        q = self.db.query(ResidModel).filter(ResidModel.codcli == cliente_id).order_by(ResidModel.id.desc())
        return [self._to_dict(x) for x in q.all()]

    def list_by_clipot(self, clipot_id: int) -> List[Dict[str, Any]]:
        q = self.db.query(ResidModel).filter(ResidModel.codcli == clipot_id).order_by(ResidModel.id.desc())
        return [self._to_dict(x) for x in q.all()]

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = ResidModel(
            codcli=data["ccliente"],
            tresiduo=data["tresiduo"],
            cantresid=data["cantresiduo"],
            pesopromres=data["pesopromres"],
            segregares=data.get("segregares"),
            numbolsas=data.get("numbolsas"),
            colorbolsa=data.get("colorbolsa"),
            observaciones=data.get("observaciones"),
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, resid_id: int, data: Dict[str, Any]) -> bool:
        obj = self.db.query(ResidModel).filter(ResidModel.id == resid_id).first()
        if not obj: return False
        obj.codcli = data["ccliente"]
        obj.tresid = data["tresiduo"]
        obj.cantresid = data["cantresiduo"]
        obj.pesopromres = data["pesopromres"]
        obj.segregares = data.get("segregares")
        obj.numbolsas = data.get("numbolsas")
        obj.observaciones = data.get("observaciones")
        self.db.commit()
        return True

    def delete(self, resid_id: int) -> bool:
        obj = self.db.query(ResidModel).filter(ResidModel.id == resid_id).first()
        if not obj: return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def _to_dict(self, r: ResidModel) -> Dict[str, Any]:
        return {
            "id": r.id,
            "ccliente": r.codcli,
            "tresiduo": r.tresid,
            "cantresiduo": r.cantresid,
            "pesopromres": r.pesopromres,
            "segregares": r.segregares,
            "numbolsas": r.numbolsas,
            "colorbolsa": r.colorbolsa,            
            "observaciones": r.observaciones,
        }
