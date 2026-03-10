from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta # type: ignore
import docxtpl # type: ignore
from pathlib import Path
import subprocess
import os

from models.ContratoCli import ContratoCli
from services.client_service import ClienteService
from services.city_service import CiudadService

MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

class ContratoService:
    def __init__(self, db: Session, template_path: str, out_dir: str):
        self.db = db
        self.template_path = Path(template_path)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def get_contrato(self, contrato_id: int):
        return (
            self.db.query(ContratoCli)
            .filter(ContratoCli.id == contrato_id)
            .first()
        )

    def get_contratos_by_cliente(self, cliente_id: int):
        return (
            self.db.query(ContratoCli)
            .filter(ContratoCli.cliente_id == cliente_id)
            .order_by(ContratoCli.id.desc())
            .all()
        )

    def crear_y_generar_pdf(self, cliente_id: int, payload):
        cli_svc = ClienteService(self.db)
        ciu_svc = CiudadService(self.db)

        cliente = cli_svc.get_cliente(cliente_id)
        if not cliente:
            return None

        ciudad_nombre = ""
        if cliente.ciudad:
            ciudad_obj = ciu_svc.get_ciudad(cliente.ciudad)
            if ciudad_obj:
                ciudad_nombre = ciudad_obj.nombre or ""

        fecha_inicio = payload.fecha_inicio
        fecha_fin = fecha_inicio + relativedelta(years=1)
        fecha_firma = payload.fecha_firma

        mes_actual = payload.mes_actual
        if not mes_actual:
            mes_actual = MESES_ES[fecha_firma.month - 1]

        base_name = f"contrato_cli_{cliente_id}_{fecha_inicio.strftime('%Y%m%d')}"
        out_docx = self.out_dir / f"{base_name}.docx"
        out_pdf = self.out_dir / f"{base_name}.pdf"

        context = {
            "razon_social": cliente.razonSocial or "",
            "nit": cliente.nit or "",
            "ciudad": ciudad_nombre,
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
            "lugar_ejecucion": payload.lugar_ejecucion or "",
            "rep_nombre": payload.rep_nombre or "",
            "rep_cc": payload.rep_cc or "",
            "rep_exp_lugar": payload.rep_exp_lugar or "",
            "dia_firma": str(fecha_firma.day),
            "mes_actual": MESES_ES[fecha_firma.month - 1],
            "anio_actual": str(fecha_firma.year),
        }

        doc = docxtpl.DocxTemplate(str(self.template_path))
        doc.render(context)
        doc.save(str(out_docx))

        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(self.out_dir),
                str(out_docx)
            ],
            check=True
        )

        if not os.path.exists(out_pdf):
            raise Exception("No se pudo generar el PDF del contrato")

        contrato = ContratoCli(
            cliente_id=cliente_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            lugar_ejecucion=payload.lugar_ejecucion,
            rep_nombre=payload.rep_nombre,
            rep_cc=payload.rep_cc,
            rep_exp_lugar=payload.rep_exp_lugar,
            fecha_firma=fecha_firma,
            mes_actual=mes_actual,
            docx_path=str(out_docx),
            pdf_path=str(out_pdf),
        )

        self.db.add(contrato)
        self.db.commit()
        self.db.refresh(contrato)

        return contrato