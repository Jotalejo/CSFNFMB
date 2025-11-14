# services/transporte_service.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import date, time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from models.FrecuenciaRec import FrecuenciaRec
from models.TipoFrecuencia import TipoFrecuencia
from models.Cliente import Cliente  # asumiendo que tiene razonSocial, direccion, lat_cli, lng_cli, ciudad...
# Si tienes Vehiculo/Persona y quieres asignación automática luego, se puede integrar.
from models.Transporte import Transporte, TransporteDetalle
from models.Vehiculo import Vehiculo
from schemas.transporte import PlanVehiculo

# Helpers
def _dia_semana_mask(dt: date) -> int:
    """
    Devuelve la máscara del día para tu convención:
    L=1, M=2, X=4, J=8, V=16, S=32, D=64
    date.weekday(): 0=Lunes ... 6=Domingo
    """
    bits = [1,2,4,8,16,32,64]
    return bits[dt.weekday()]

def _parse_dias_mes(s: Optional[str]) -> set[int]:
    if not s:
        return set()
    out = set()
    for token in s.split(','):
        token = token.strip()
        if not token:
            continue
        try:
            n = int(token)
            if 1 <= n <= 31:
                out.add(n)
        except:
            pass
    return out

def build_google_maps_url(clientes: List[Dict[str, Any]]) -> Optional[str]:
    """
    Construye un URL de Google Maps con waypoints.
    Espera clientes con lat/lng. Si faltan coords, retorna None.
    """
    waypoints = []
    for c in clientes:
        lat = c.get("lat")
        lng = c.get("lng")
        if lat is None or lng is None:
            return None
        waypoints.append(f"{lat},{lng}")

    if not waypoints:
        return None

    # origen/destino en Barrancabermeja (ajusta si quieres)
    origin = "Barrancabermeja,Santander"
    destination = "Barrancabermeja,Santander"
    wp = "|".join(waypoints)

    # URL para abrir en una pestaña con ruta y paradas
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin}"
        f"&destination={destination}"
        f"&waypoints={wp}"
    )

class TransporteService:
    def __init__(self, db: Session):
        self.db = db

    def clientes_programados_para(self, dt: date) -> List[Dict[str, Any]]:
        """
        Selecciona los clientes que deben visitarse en la fecha 'dt'
        basándose en frecuenciarec:
          - tipo diaria -> siempre entra
          - tipo semanal -> verifica bitmask del día
          - tipo mensual -> verifica si el día (1..31) está en dias_mes
        Retorna una lista de dicts “planilla”.
        """
        # Traemos frecuencias activas + tipo + cliente
        freqs: List[FrecuenciaRec] = (
            self.db.query(FrecuenciaRec)
            .join(TipoFrecuencia, FrecuenciaRec.tipo)
            .options(
                joinedload(FrecuenciaRec.tipo),
                # si quieres cargar cliente via relationship, define en el modelo y usa joinedload
            )
            .filter(FrecuenciaRec.activo == 1)
            .all()
        )

        dia_mask = _dia_semana_mask(dt)
        dia_mes_actual = dt.day

        # Pre-cargamos los clientes por id (si no declaraste relationship)
        cliente_ids = list({f.cliente_id for f in freqs})
        clientes_map: Dict[int, Cliente] = {}
        if cliente_ids:
            cls = (
                self.db.query(Cliente)
                .filter(Cliente.id.in__(cliente_ids))
                .all()
            )
            clientes_map = {c.id: c for c in cls}

        planilla: List[Dict[str, Any]] = []
        for f in freqs:
            tf = f.tipo  # TipoFrecuencia
            if not tf or not f.cliente_id:
                continue

            incluir = False
            nombre_tipo = (tf.nombre or '').strip().lower()

            if nombre_tipo == 'diaria':
                incluir = True
            elif nombre_tipo == 'semanal':
                # match bitwise
                if f.diasem_mask and (f.diasem_mask & dia_mask) > 0:
                    incluir = True
            elif nombre_tipo == 'mensual':
                dias = _parse_dias_mes(f.dias_mes)
                if dia_mes_actual in dias:
                    incluir = True
            else:
                # por si hay otros tipos, los ignoramos
                pass

            if not incluir:
                continue

            c = clientes_map.get(f.cliente_id)
            if not c:
                continue

            item = {
                "cliente_id": c.id,
                "cliente": getattr(c, "razonSocial", None),
                "direccion": getattr(c, "direccion", None),
                "telefono": getattr(c, "telefono", None),
                "ciudad": getattr(c, "ciudad", None),
                "hora_desde": f.hora_desde,
                "hora_hasta": f.hora_hasta,
                "veces": f.veces,
                "capacidad_kg": f.capacidad_kg,
                "observ": f.observ,
                # coords (si las tienes en tu modelo Cliente)
                "lat": getattr(c, "lat", None) or getattr(c, "lat_cli", None),
                "lng": getattr(c, "lng", None) or getattr(c, "lng_cli", None),
            }
            planilla.append(item)

        # si TODAS tienen coords, arma link para rutear
        ruta_google = build_google_maps_url(planilla) if planilla else None
        for p in planilla:
            p["ruta_google"] = ruta_google

        return planilla

    def guardar_plan(self, fecha: date, plan: List[PlanVehiculo]) -> int:
        """
        Crea una fila Transporte por cada grupo de vehículo y detalla sus paradas.
        Devuelve cuántos registros de transporte se crearon.
        """
        creados = 0
        for grupo in plan:
            veh_id = None
            if grupo.vehiculo and grupo.vehiculo.get("id"):
                veh_id = int(grupo.vehiculo["id"])

            # Encabezado (uno por vehículo)
            tr = Transporte(
                recoleccion_id=None,
                ruta=f"{fecha.isoformat()}",
                hora_inicio=None,
                hora_fin=None,
                observ=f"Plan {fecha.isoformat()}",
                vehiculo_id=veh_id if veh_id else None
            )
            self.db.add(tr)
            self.db.flush()  # para obtener tr.id

            # Detalles
            for p in grupo.paradas:
                det = TransporteDetalle(
                    transporte_id=tr.id,
                    fecha=fecha,
                    cliente_id=p.cliente_id,
                    orden=p.orden,
                    direccion=p.direccion,
                    hora_pref=p.hora_pref,
                    ventana_ini=p.ventana_ini,
                    ventana_fin=p.ventana_fin,
                    capacidad_kg=p.capacidad_kg,
                    lat=str(p.lat) if p.lat is not None else None,
                    lng=str(p.lng) if p.lng is not None else None,
                )
                self.db.add(det)

            creados += 1

        self.db.commit()
        return creados
