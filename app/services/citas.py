# services/citas.py
# services/citas.py
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime, date, time
from models.Citas import Cita as CitaModel
from schemas.Citas import CitaCreate, Cita as CitaSchema

# ---------- Helpers de parseo ----------
def _parse_date(v: Optional[str]) -> Optional[date]:
    if not v: return None
    return datetime.strptime(v, "%Y-%m-%d").date()

def _parse_time(v: Optional[str]) -> Optional[time]:
    if not v: return None
    # acepta "HH:MM" o "HH:MM:SS"
    fmt = "%H:%M:%S" if len(v.strip()) == 8 else "%H:%M"
    return datetime.strptime(v.strip(), fmt).time()

class CitaService:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Lecturas ----------
    def get_citas(self) -> List[Dict[str, Any]]:
        q = (self.db.query(CitaModel)
             .order_by(CitaModel.fechacita.desc().nullslast(),
                       CitaModel.horacita.desc().nullslast()))
        return [self._to_dict(x) for x in q.all()]

    def get_cita(self, cita_id: int) -> Optional[Dict[str, Any]]:
        x = self.db.query(CitaModel).filter(CitaModel.id == cita_id).first()
        return self._to_dict(x) if x else None

    def list_by_clipot(self, clipot_id: int) -> List[Dict[str, Any]]:
        q = (self.db.query(CitaModel)
             .filter(CitaModel.clipot == clipot_id)
             .order_by(CitaModel.fechacita.desc().nullslast()))
        return [self._to_dict(x) for x in q.all()]

    def list_by_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        q = (self.db.query(CitaModel)
             .filter(CitaModel.cliente == cliente_id)
             .order_by(CitaModel.fechacita.desc().nullslast()))
        return [self._to_dict(x) for x in q.all()]

    # ---------- Crear / Actualizar desde JSON (Schemas) ----------
    def create(self, payload: CitaCreate) -> Dict[str, Any]:
        obj = CitaModel(**payload.model_dump(exclude_unset=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update(self, cita_id: int, payload: CitaSchema) -> Optional[Dict[str, Any]]:
        obj = self.db.query(CitaModel).filter(CitaModel.id == cita_id).first()
        if not obj:
            return None
        for field, val in payload.model_dump(exclude_unset=True).items():
            setattr(obj, field, val)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ---------- Crear / Actualizar desde FORM (tu wizard) ----------
    def create_from_form(self, form: Dict[str, Any]) -> Dict[str, Any]:
        data = self._map_form_to_model(form)
        obj = CitaModel(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    def update_from_form(self, cita_id: int, form: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        obj = self.db.query(CitaModel).filter(CitaModel.id == cita_id).first()
        if not obj:
            return None
        data = self._map_form_to_model(form)
        for k, v in data.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return self._to_dict(obj)

    # ---------- Borrar ----------
    def delete(self, cita_id: int) -> bool:
        obj = self.db.query(CitaModel).filter(CitaModel.id == cita_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ---------- Mapeo de nombres de FORM -> modelo ----------
    def _map_form_to_model(self, f: Dict[str, Any]) -> Dict[str, Any]:
        """
        Espera los 'name' del HTML que mostraste:
          clipot_id, cliente_id, fecprogc, horaprogc, asuncita, tipodv,
          horaIncit, horafincit, actpend, fecsegap, actrealiz, loscompr, fecsegap2,
          lugarc, ubicacc, tipogen, ciudadc, regcit, observ
        """
        def _int(x): 
            try: return int(x) if x not in (None, "", "null") else None
            except: return None

        return {
            "clipot":        _int(f.get("clipot_id")),
            "cliente":       _int(f.get("cliente_id")),

            "fechacita":     _parse_date(f.get("fecprogc")),
            "horacita":      _parse_time(f.get("horaprogc")),
            "asuntocita":    (f.get("asuncita") or None),

            "tipodevisi":    _int(f.get("tipodv")),
            "iniciocita":    _parse_time(f.get("horaIncit")),
            "fincita":       _parse_time(f.get("horafincit")),

            "actpendcita":   (f.get("actpend") or None),
            "seguiapcita":   _parse_date(f.get("fecsegap")),

            "actrealcita":   (f.get("actrealiz") or None),
            "compromcita":   (f.get("loscompr") or None),
            "fecompromcita": _parse_date(f.get("fecsegap2")),

            "lugarcita":     (f.get("lugarc") or None),
            "ubiccita":      (f.get("ubicacc") or None),

            "tipogen":       _int(f.get("tipogen")),
            "ciudad":        _int(f.get("ciudadc")),
            "regioncita":    (f.get("regcit") or None),
            "observaciones": (f.get("observ") or None),
        }

    # ---------- Serializador ----------
    def _to_dict(self, c: Optional[CitaModel]) -> Optional[Dict[str, Any]]:
        if not c: return None
        return {
            "id": c.id,
            "clipot": c.clipot,
            "cliente": c.cliente,

            "fechacita": c.fechacita.isoformat() if c.fechacita else None,
            "horacita": c.horacita.isoformat() if c.horacita else None,
            "asuntocita": c.asuntocita,

            "tipodevisi": c.tipodevisi,
            "iniciocita": c.iniciocita.isoformat() if c.iniciocita else None,
            "fincita": c.fincita.isoformat() if c.fincita else None,

            "actpendcita": c.actpendcita,
            "seguiapcita": c.seguiapcita.isoformat() if c.seguiapcita else None,

            "actrealcita": c.actrealcita,
            "compromcita": c.compromcita,
            "fecompromcita": c.fecompromcita.isoformat() if c.fecompromcita else None,

            "lugarcita": c.lugarcita,
            "ubiccita": c.ubiccita,

            "tipogen": c.tipogen,
            "ciudad": c.ciudad,
            "regioncita": c.regioncita,
            "observaciones": c.observaciones,
        }
