# services/plan_transporte_service.py
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional, Dict
from models.FrecuenciaRec import FrecuenciaRec
from models.TipoFrecuencia import TipoFrecuencia
from models.Cliente import Cliente
from models.Vehiculo import Vehiculo
from schemas.transporte import PlanVehiculo, PlanParada
import calendar

class PlanTransporteService:
    def __init__(self, db: Session):
        self.db = db

    # ----- Helpers -----
    @staticmethod
    def weekday_18n(d: date) -> int:
        """
        Devuelve 1..7 (L=1 .. D=7) para ser compatible con tu máscara.
        datetime.weekday(): L=0 .. D=6
        """
        return d.weekday() + 1

    @staticmethod
    def aplica_fecha(frec: FrecuenciaRec, fecha: date, nombre_tipo: str) -> bool:
        # diaria
        if nombre_tipo == "diaria":
            # si quieres, respeta hora_hasta/hora_desde solo para ventana
            return True

        # semanal: validar máscara vs día de la semana
        if nombre_tipo == "semanal":
            if not frec.diasem_mask:
                return False
            dow = PlanTransporteService.weekday_18n(fecha)  # 1..7
            return (frec.diasem_mask & FrecuenciaRec.to_mask([dow])) != 0

        # mensual: validar día del mes en la lista
        if nombre_tipo == "mensual":
            if not frec.dias_mes:
                return False
            try:
                dias = [int(x.strip()) for x in frec.dias_mes.split(",") if x.strip()]
                return fecha.day in dias
            except:
                return False

        return False

    # ----- Generar plan -----
    def generar_plan(self, fecha: date, vehiculo_id: Optional[int] = None) -> List[PlanVehiculo]:
        # 1) Vehículos disponibles:
        vehiculos = []
        if vehiculo_id:
            v = self.db.query(Vehiculo).get(vehiculo_id)
            if v: vehiculos = [v]
        else:
            vehiculos = self.db.query(Vehiculo).order_by(Vehiculo.id.asc()).all()

        # fallback: si no hay vehículos, igual devolvemos un "bucket" sin asignar
        buckets: List[PlanVehiculo] = []
        if vehiculos:
            for v in vehiculos:
                buckets.append(PlanVehiculo(vehiculo={"id": v.id, "placa": v.placa, "capacidad": v.capacidad}, paradas=[]))
        else:
            buckets.append(PlanVehiculo(vehiculo=None, paradas=[]))

        # 2) Traer frecuencias activas y decidir si aplican
        #    Hacemos join con TipoFrecuencia y Cliente para nombres y direcciones
        frecs = (
            self.db.query(FrecuenciaRec)
            .join(TipoFrecuencia, FrecuenciaRec.tipo_id == TipoFrecuencia.id)
            .join(Cliente, FrecuenciaRec.cliente_id == Cliente.id)  # ojo: si tu PK es cod_cli, ajusta
            .filter(FrecuenciaRec.activo == 1)
            .all()
        )

        candidatos: List[Dict] = []
        for f in frecs:
            tipo_nombre = f.tipo.nombre  # "diaria", "semanal", "mensual"
            if self.aplica_fecha(f, fecha, tipo_nombre):
                c = self.db.query(Cliente).get(f.cliente_id)
                if not c: 
                    continue
                
                candidatos.append({
                    "cliente_id": c.id,  # ajustar si tu PK es cod_cli
                    "cliente_nombre": getattr(c, "razonSocial", None),
                    "direccion": getattr(c, "direccion", None),
                    "lat": getattr(c, "latrecolec_cli", None),
                    "lng": getattr(c, "lngrecolec_cli", None),
                    "hora_pref": f.hora_desde,
                    "ventana_ini": f.hora_desde,
                    "ventana_fin": f.hora_hasta,
                    "capacidad_kg": f.capacidad_kg,
                })

        # 3) Asignación simple a vehículos (round-robin con control básico de capacidad)
        #    Acumula la carga por vehículo y evita exceder demasiado.
        if not candidatos:
            return buckets

        carga = [0] * len(buckets)
        idx = 0
        for cand in candidatos:
            asignado = False
            # intento: encontrar bucket con capacidad suficiente o el más "liviano"
            mejor_i = None
            mejor_gap = None
            for i, b in enumerate(buckets):
                cap = b.vehiculo.get("capacidad") if (b.vehiculo) else None
                # si no hay capacidad definida, lo aceptamos
                if not cap:
                    mejor_i = i
                    break
                gap = cap - (carga[i] + (cand.get("capacidad_kg") or 0))
                if gap >= 0:
                    mejor_i = i
                    break
                # si ninguno alcanza, elige el de mayor gap (menos malo)
                if mejor_gap is None or gap > mejor_gap:
                    mejor_gap = gap
                    mejor_i = i

            i = mejor_i if mejor_i is not None else 0
            p = PlanParada(
                recoleccion_id=None,
                cliente_id=cand["cliente_id"],
                cliente_nombre=cand["cliente_nombre"] or "",
                direccion=cand["direccion"] or "",
                lat=cand["lat"], lng=cand["lng"],
                hora_pref=cand["hora_pref"],
                ventana_ini=cand["ventana_ini"],
                ventana_fin=cand["ventana_fin"],
                capacidad_kg=cand["capacidad_kg"],
                orden=(len(buckets[i].paradas) + 1)
            )
            buckets[i].paradas.append(p)
            carga[i] += (cand.get("capacidad_kg") or 0)
            idx = (idx + 1) % len(buckets)

        return buckets
