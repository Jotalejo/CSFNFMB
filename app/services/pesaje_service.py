from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta

from models import (
    Pesaje,
    DetallePesaje,
    Recoleccion,
    DetalleRecoleccion,
    Cliente,
    Vehiculo,
    TipoResiduo,
)

from schemas.pesaje import PesajeCreate


class PesajeService:
    def __init__(self, db: Session):
        self.db = db

    def get_vehiculos_por_fecha(self, fecha):
        return (
            self.db.query(Vehiculo)
            .join(Recoleccion, Recoleccion.vehiculo == Vehiculo.id)
            .filter(Recoleccion.fecha == fecha)
            .distinct()
            .order_by(Vehiculo.placa)
            .all()
        )

    def get_clientes_por_fecha_vehiculo(self, fecha, vehiculo_id: int):
        return (
            self.db.query(Cliente)
            .join(Recoleccion, Recoleccion.cliente == Cliente.id)
            .filter(Recoleccion.fecha == fecha)
            .filter(Recoleccion.vehiculo == vehiculo_id)
            .distinct()
            .order_by(Cliente.razonSocial)
            .all()
        )

    def get_manifiestos(self, fecha, vehiculo_id: int, cliente_id: int):
        return (
            self.db.query(Recoleccion)
            .outerjoin(Pesaje, Pesaje.recoleccion_id == Recoleccion.id)
            .filter(Recoleccion.fecha == fecha)
            .filter(Recoleccion.vehiculo == vehiculo_id)
            .filter(Recoleccion.cliente == cliente_id)
            .filter(
                (Pesaje.id == None) | (Pesaje.estado != "CONFIRMADO")
            )
            .order_by(Recoleccion.id.desc())
            .all()
        )

    def get_detalle_manifiesto(self, recoleccion_id: int):
        return (
            self.db.query(DetalleRecoleccion)
            .join(TipoResiduo, DetalleRecoleccion.tipo_residuo_id == TipoResiduo.id)
            .filter(DetalleRecoleccion.recoleccion_id == recoleccion_id)
            .all()
        )

    def crear_pesaje(self, data: PesajeCreate):
        db_pesaje = Pesaje(
            recoleccion_id=data.recoleccion_id,
            vehiculo_id=data.vehiculo_id,
            cliente_id=data.cliente_id,
            fecha=data.fecha,
            estado=data.estado or "PENDIENTE",
            firma_verificacion=data.firma_verificacion,
            observaciones=data.observaciones,
        )

        self.db.add(db_pesaje)
        self.db.flush()

        for item in data.detalles or []:
            db_detalle = DetallePesaje(
                pesaje_id=db_pesaje.id,
                detalle_recoleccion_id=item.detalle_recoleccion_id,
                tipo_residuo_id=item.tipo_residuo_id,
                bolsas=item.bolsas,
                peso=item.peso,
                confirmado=item.confirmado or 0,
                observaciones=item.observaciones,
            )
            self.db.add(db_detalle)

        self.db.commit()
        self.db.refresh(db_pesaje)

        return db_pesaje

    def acumulado_dia(self, fecha):
        return (
            self.db.query(func.sum(DetallePesaje.peso))
            .join(Pesaje, Pesaje.id == DetallePesaje.pesaje_id)
            .filter(Pesaje.fecha == fecha)
            .scalar()
            or 0
        )

    def acumulado_semana(self, fecha):
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        return (
            self.db.query(func.sum(DetallePesaje.peso))
            .join(Pesaje, Pesaje.id == DetallePesaje.pesaje_id)
            .filter(Pesaje.fecha >= inicio_semana)
            .filter(Pesaje.fecha <= fin_semana)
            .scalar()
            or 0
        )

    def acumulado_mes(self, fecha):
        inicio_mes = fecha.replace(day=1)

        if fecha.month == 12:
            inicio_mes_siguiente = fecha.replace(
                year=fecha.year + 1,
                month=1,
                day=1
            )
        else:
            inicio_mes_siguiente = fecha.replace(
                month=fecha.month + 1,
                day=1
            )

        return (
            self.db.query(func.sum(DetallePesaje.peso))
            .join(Pesaje, Pesaje.id == DetallePesaje.pesaje_id)
            .filter(Pesaje.fecha >= inicio_mes)
            .filter(Pesaje.fecha < inicio_mes_siguiente)
            .scalar()
            or 0
        )
    
    def acumulados_por_cliente(self, fecha, cliente_id=None):
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        inicio_mes = fecha.replace(day=1)

        if fecha.month == 12:
            inicio_mes_siguiente = fecha.replace(
                year=fecha.year + 1,
                month=1,
                day=1
            )
        else:
            inicio_mes_siguiente = fecha.replace(
                month=fecha.month + 1,
                day=1
            )

        base = (
            self.db.query(
                Cliente.id.label("cliente_id"),
                Cliente.razonSocial.label("cliente"),
                func.sum(DetallePesaje.peso).label("kg")
            )
            .join(Pesaje, Pesaje.cliente_id == Cliente.id)
            .join(DetallePesaje, DetallePesaje.pesaje_id == Pesaje.id)
            .filter(Pesaje.estado == "CONFIRMADO")
        )

        if cliente_id:
            base = base.filter(Cliente.id == cliente_id)

        def consultar(query, desde, hasta=None):
            q = query.filter(Pesaje.fecha >= desde)
            if hasta:
                q = q.filter(Pesaje.fecha <= hasta)
            else:
                q = q.filter(Pesaje.fecha == desde)

            return (
                q.group_by(Cliente.id, Cliente.razonSocial)
                .order_by(Cliente.razonSocial)
                .all()
            )

        dia = consultar(base, fecha, None)
        semana = consultar(base, inicio_semana, fin_semana)
        mes = (
            base
            .filter(Pesaje.fecha >= inicio_mes)
            .filter(Pesaje.fecha < inicio_mes_siguiente)
            .group_by(Cliente.id, Cliente.razonSocial)
            .order_by(Cliente.razonSocial)
            .all()
        )

        return {
            "dia": dia,
            "semana": semana,
            "mes": mes,
        }