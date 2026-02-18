from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from schemas.Recolecc import RecolectCreate
from dependencies import templates
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from services import RecoleccService, ClienteService, VehiculoService
from services.tiposresid import TipoResidService
from schemas.Tiporesid import TipoResidOut
from models.Recoleccion import Recoleccion as RecoleccionModel
from models.FrecuenciaRec import FrecuenciaRec
import pdfkit
import os

router = APIRouter(
    prefix="/recolecciones",
    tags=["recoleccion"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para la recolección


@router.get("/")
async def get_recolecc(request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    clientService = ClienteService(db)
    vehiculoService = VehiculoService(db)
    recolecciones = service.get_recolecc()
    clientes = clientService.get_clientes()
    vehiculos = vehiculoService.options()
    return templates.TemplateResponse("/recolecci/recolecc.html", {"request": request, "recolecciones": recolecciones, "clientes": clientes, "vehiculos": vehiculos})


@router.get("/detalle/{rec_id}", response_class=HTMLResponse)
def detalle_recoleccion(rec_id: int, request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    r = service.get_recolecc_by_id(rec_id)
    if not r:
        raise HTTPException(
            status_code=404, detail="Recolección no encontrada")
    # Renderiza un parcial (solo el cuerpo del modal)
    return templates.TemplateResponse("recolecci/_detalle_modal.html", {"request": request, "r": r})


@router.get("/tiposresiduo/{cliente_id}", response_model=List[TipoResidOut])
def tipos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return TipoResidService(db).list_by_cliente(cliente_id)

# routers/recolecc.py (fragmento del POST)

@router.post("/", response_class=RedirectResponse)

async def crear_recolecc(
    request: Request,
    createData: RecolectCreate,
    db: Session = Depends(get_db)
):

    # ... validaciones y parsing hora ...

    RecoleccService(db).create_recolecc(createData)
    return RedirectResponse(url="/recolecciones/", status_code=303)


@router.get("/manifiesto/{recoleccion_id}")
def get_manifiesto(recoleccion_id: int, request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    recoleccion = service.get_recolecc_by_id(recoleccion_id)
    cliente = recoleccion.cliente_rel

    from models.FrecuenciaRec import FrecuenciaRec
    from models.TipoFrecuencia import TipoFrecuencia

    def decode_diasem_mask(mask: int | None) -> str:
        # bits: 1=Lun,2=Mar,4=Mié,8=Jue,16=Vie,32=Sáb,64=Dom
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        if not mask:
            return ""
        seleccionados = [dias[i] for i in range(7) if mask & (1 << i)]
        return "Lun–Dom" if len(seleccionados) == 7 else ", ".join(seleccionados)

    def parse_dias_mes(txt: str | None) -> str:
        if not txt:
            return ""
        parts = [p.strip() for p in txt.split(",") if p.strip()]
        return ", ".join(parts)

    def fmt_hora(t) -> str:
        return t.strftime("%H:%M") if t else ""

    def build_frecuencia_str(freq) -> str:
        tipo_nombre = (freq.tipo.nombre if freq.tipo else "").strip().lower()

        hd = fmt_hora(freq.hora_desde)
        hh = fmt_hora(freq.hora_hasta)
        ventana = f" {hd}–{hh}" if hd and hh else (f" desde {hd}" if hd else "")

        veces_txt = f" x{freq.veces}" if freq.veces else ""

        if tipo_nombre == "diaria":
            dias_txt = decode_diasem_mask(freq.diasem_mask) or "Todos los días"
            return f"Diaria ({dias_txt}){ventana}{veces_txt}"

        if tipo_nombre == "semanal":
            dias_txt = decode_diasem_mask(freq.diasem_mask) or "—"
            return f"Semanal ({dias_txt}){ventana}{veces_txt}"

        if tipo_nombre == "mensual":
            diasmes = parse_dias_mes(freq.dias_mes)
            dias_txt = f"Días {diasmes}" if diasmes else "—"
            return f"Mensual ({dias_txt}){ventana}{veces_txt}"

        return f"{freq.tipo.nombre if freq.tipo else 'Frecuencia'}{ventana}{veces_txt}"

    # 1) Buscar frecuencia activa del cliente (si hay varias, usa la más reciente)
    freq = (
        db.query(FrecuenciaRec)
        .filter(FrecuenciaRec.cliente_id == cliente.id)
        .filter(FrecuenciaRec.activo == 1)
        .order_by(FrecuenciaRec.id.desc())
        .first()
    )

    frecuencia_txt = ""
    if freq:
        tf = db.query(TipoFrecuencia).filter(TipoFrecuencia.id == freq.tipo_id).first()        
        tipo_nombre = (getattr(freq.tipo, "nom_tfrec", None) or getattr(freq.tipo, "nombre", None) or "").strip().lower()
        frecuencia_txt = build_frecuencia_str(freq) if freq else ""
    else:
        frecuencia_txt = ""

    options = {
        # ancho tipo tirilla ~ 1/3 carta
        'page-width': '72mm',
        # alto grande (wkhtmltopdf no maneja "auto" bien en height)
        'page-height': '297mm',  # puedes subirlo si el manifiesto sale largo

        # márgenes pequeños para tirilla
        'margin-top': '5mm',
        'margin-right': '5mm',
        'margin-bottom': '5mm',
        'margin-left': '5mm',

        'enable-local-file-access': None,
        'encoding': 'UTF-8',
        'quiet': ''
    }

    if not recoleccion:
        raise HTTPException(
            status_code=404, detail="Recolección no encontrada")

    # Usar ruta absoluta del sistema de archivos para wkhtmltopdf
    logo_path = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), 'static', 'assets', 'images', 'logo_gresab.png')
    logo_url = f"file://{logo_path}" if os.path.exists(logo_path) else ""

    residuos = []
    cantidad_total = 0
    peso_total = 0.0
    for detalle in recoleccion.detalles:
        residuos.append({
            "tipo": detalle.tipo_residuo.nombre,
            "cantidad": detalle.cantidad,
            "kilos": detalle.peso
        })
        cantidad_total += detalle.cantidad
        peso_total += detalle.peso

    placa = recoleccion.vehiculo_rel.placa if recoleccion.vehiculo_rel else ""
    
    fecha_txt = recoleccion.fecha.strftime("%Y-%m-%d") if recoleccion.fecha else ""
    hora_txt = recoleccion.hora.strftime("%H:%M:%S") if recoleccion.hora else ""
    fecha_recoleccion = f"{fecha_txt} {hora_txt}".strip()

    cliente_data = {
    "id": getattr(cliente, "id", ""),
    "razonSocial": getattr(cliente, "razonSocial", ""),
    "direccion": getattr(cliente, "direccion", ""),
    "ciudad": getattr(cliente, "ciudad", ""),        # ojo: puede ser ID
    #"frecuencia": getattr(cliente, "frecuencia", ""),# si no existe, queda vacío
    "frecuencia": frecuencia_txt,
    "nit": getattr(cliente, "nit", ""),
    "firma_nombre": getattr(cliente, "firma_nombre", ""),
    "firma_cc": getattr(cliente, "firma_cc", ""),
    }

    data = {
        "request": request,
        "empresa": {
            "nombre": "GRESAB SAS",
            "direccion1": "Planta: Km 8 Vía El Centro Ecopetrol",
            "pbx1": "320 580 31 02",
            "ciudad1": "Barrancabermeja - Colombia",
            "direccion2": "Oficina : Carrera 13 # 49 - 20",
            "pbx2": "gresabgerencia@gmail.com",
            "nit": "901.999.012-4",
            "web": "www.gresab.com",
            "logo_url": logo_url
        },
        "manifiesto": {
            "fecha": fecha_recoleccion,
            "numero": recoleccion.id
        },
        "cliente": cliente_data,
        "operario": {
            "nombre": "",
            "cc": ""
        },
        "auxiliar": {
            "nombre": "",
            "cc": ""
        },
        "vehiculo": {
            "placa": placa,
        },
        "residuos": residuos,
        "totales": {
            "cantidad": cantidad_total,
            "kilos": peso_total
        }
    }

    from models.Ciudad import Ciudad as CiudadModel

    ciudad_nombre = ""
    if getattr(cliente, "ciudad", None):
        ciu = db.query(CiudadModel).filter(CiudadModel.id == cliente.ciudad).first()
        ciudad_nombre = getattr(ciu, "nombre", "") if ciu else ""

    cliente_data["ciudad"] = ciudad_nombre
    

    template = templates.env.get_template("/recolecci/manifiesto.html")
    html = template.render(data)
    pdf = pdfkit.from_string(html, False, options=options)
    headers = {'Content-Disposition': 'attachment; filename="certificado.pdf"'}
    return Response(pdf, headers=headers, media_type='application/pdf')


@router.post("/")
def crear_recoleccion(
    request: Request,
    cliente_id: int = Form(...),
    fecha: date = Form(...),
    tipo_residuo_id: List[int] = Form(...),
    cantbol: List[float] = Form(...),
    pesobol: List[float] = Form(...),
    totpeso: Optional[List[float]] = Form(None),
    observ: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    # estado por defecto = 1
    for i in range(len(tipo_residuo_id)):
        rec = RecoleccionModel(
            cliente=cliente_id,
            fecha=fecha,
            tresiduo=tipo_residuo_id[i],
            cantresiduo=cantbol[i],
            peso=totpeso[i] if totpeso and i < len(
                totpeso) and totpeso[i] is not None else (cantbol[i]*pesobol[i]),
            estado_id=1,
            observaciones=observ
        )
        db.add(rec)
    db.commit()
    return RedirectResponse(url="/recolecciones/", status_code=303)
