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

# @router.get("/new")
# async  def add_recolecc():
# @router.get("/new")
# async  def add_recolecc():
#    return "Grabando una recolección"


@router.get("/tiposresiduo/{cliente_id}", response_model=List[TipoResidOut])
def tipos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return TipoResidService(db).list_by_cliente(cliente_id)

# routers/recolecc.py (fragmento del POST)


@router.post("/", response_class=RedirectResponse)
# async def crear_recolecc(
#    request: Request,
#    db: Session = Depends(get_db),
#
#    cliente_id: int = Form(...),
#    fecha: Optional[date] = Form(None),
#    hora: Optional[str] = Form(None),
#    tipo_residuo_id: int = Form(...),
#
#    cantbol: Optional[int] = Form(None),
#    pesobol: Optional[float] = Form(None),
#    totpeso: Optional[float] = Form(None),
#
#    estado_id: Optional[int] = Form(None),
#    vehiculo_id: Optional[int] = Form(None),
#    codigo_bar: Optional[str] = Form(None),
#    firma_entrega: Optional[str] = Form(None),
#    lafirmaderecibo: Optional[str] = Form(None),   # ⬅️ nuevo en el form
#    observ: Optional[str] = Form(None),
# ):
async def crear_recolecc(
    request: Request,
    createData: RecolectCreate,
    db: Session = Depends(get_db)
):

    # ... validaciones y parsing hora ...

    #    payload = RecolectCreate(
    #        cliente=cliente_id,
    #        fecha=fecha,
    #        # hora=hora_obj, # type: ignore
    #        tresiduo=tipo_residuo_id,
    #        cantresiduo=cantbol,
    #        peso=totpeso,
    #        estado_id=estado_id,
    #        vehiculo=vehiculo_id,
    #        codigobar=codigo_bar,
    #        firmarecolec=firma_entrega,
    #        lafirmaderecibo=lafirmaderecibo,   # ⬅️ aquí viaja al schema/model
    #        observaciones=observ,
    #    ){"cliente_id":"9","fecha":"2025-11-15","email":"hseq@unidadclinicasannicolas.com","conta":"DR.TAZO","teldco":"3202605856","observ":"test","btnguardc":"","tablaResiduos":[{"tipo_residuo_id":"11","cantbol":"12","pesobol":"1","totpeso":"12.00"},{"tipo_residuo_id":"1","cantbol":"2","pesobol":"21","totpeso":"42.00"}]}
    #
    RecoleccService(db).create_recolecc(createData)
    return RedirectResponse(url="/recolecciones/", status_code=303)


@router.get("/manifiesto/{recoleccion_id}")
def get_manifiesto(recoleccion_id: int, request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    recoleccion = service.get_recolecc_by_id(recoleccion_id)
    cliente = recoleccion.cliente_rel

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'enable-local-file-access': None,
        'no-stop-slow-scripts': None,
        'debug-javascript': None,
        'javascript-delay': 1000,
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
    fecha_recoleccion = recoleccion.fecha.strftime("%Y-%m-%d") if recoleccion.fecha else ""
    fecha_recoleccion = fecha_recoleccion + recoleccion.hora.strftime("%H:%M:%S") if recoleccion.hora else ""

    data = {
        "request": request,
        "empresa": {
            "nombre": "GRESAB SAS ESP R-152-01",
            "direccion1": "Cr. 38A No. 48a-71",
            "pbx1": "(7) 643 9999",
            "ciudad1": "Barrancabermeja - Colombia",
            "direccion2": "Cl. 17b No. 39-75",
            "pbx2": "(1) 244 4000",
            "ciudad2": "Pereira - Colombia",
            "nit": "804002433-1",
            "web": "www.selectiva.net.co",
            "logo_url": logo_url
        },
        "manifiesto": {
            "fecha": fecha_recoleccion,
            "numero": recoleccion.id
        },
        "cliente": cliente.razonSocial,
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

    template = templates.env.get_template("/recolecci/manifiesto.html")
    html = template.render(data)
    pdf = pdfkit.from_string(html, False, options=options)
    headers = {'Content-Disposition': 'attachment; filename="certificado.pdf"'}
    return Response(pdf, headers=headers, media_type='application/pdf')

    # return templates.TemplateResponse("/recolecci/manifiesto.html", data)


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
