from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from schemas.Recolecc import RecolectCreate
from dependencies import templates
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from services import RecoleccService, ClienteService
from services.tiposresid import TipoResidService
from schemas.Tiporesid import TipoResidOut
from models.Recoleccion import Recoleccion as RecoleccionModel

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
    recolecciones = service.get_recolecc()
    clientes = clientService.get_clientes()
    return templates.TemplateResponse("/recolecci/recolecc.html", {"request": request, "recolecciones": recolecciones, "clientes": clientes})

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
async def crear_recolecc(
    request: Request,
    db: Session = Depends(get_db),

    cliente_id: int = Form(...),
    fecha: Optional[date] = Form(None),
    hora: Optional[str] = Form(None),
    tipo_residuo_id: int = Form(...),

    cantbol: Optional[int] = Form(None),
    pesobol: Optional[float] = Form(None),
    totpeso: Optional[float] = Form(None),

    estado_id: Optional[int] = Form(None),
    vehiculo_id: Optional[int] = Form(None),
    codigo_bar: Optional[str] = Form(None),
    firma_entrega: Optional[str] = Form(None),
    lafirmaderecibo: Optional[str] = Form(None),   # ⬅️ nuevo en el form
    observ: Optional[str] = Form(None),
):
    # ... validaciones y parsing hora ...

    payload = RecolectCreate(
        cliente=cliente_id,
        fecha=fecha,
        # hora=hora_obj, # type: ignore
        tresiduo=tipo_residuo_id,
        cantresiduo=cantbol,
        peso=totpeso,
        estado_id=estado_id,
        vehiculo=vehiculo_id,
        codigobar=codigo_bar,
        firmarecolec=firma_entrega,
        lafirmaderecibo=lafirmaderecibo,   # ⬅️ aquí viaja al schema/model
        observaciones=observ,
    )

    RecoleccService(db).create_recolecc(payload)
    return RedirectResponse(url="/recolecciones/", status_code=303)


@router.get("/manifiesto/{recoleccion_id}")
def get_manifiesto(recoleccion_id: int, request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    recoleccion = service.get_recoleccion_detallada(recoleccion_id)
    cliente = recoleccion.cliente_rel

    logo_url = "/static/assets/images/logo_gresab.png"

    data = {
        "request": request,
        "empresa": {
            "nombre": "DESCONT SAS ESP R-152-01",
            "direccion1": "Cr. 38A No. 48a-71",
            "pbx1": "(7) 643 9999",
            "ciudad1": "Bucaramanga - Colombia",
            "direccion2": "Cl. 17b No. 39-75",
            "pbx2": "(1) 244 4000",
            "ciudad2": "Bogotá - Colombia",
            "nit": "804002433-1",
            "web": "www.descont.com.co",
            "logo_url": logo_url
        },
        "manifiesto": {
            "fecha": "2019-12-06 13:04:26",
            "numero": "3323618"
        },
        "cliente": cliente,
        "operario": {
            "nombre": "Marlon Cardona Angarita",
            "cc": "1098657224"
        },
        "auxiliar": {
            "nombre": "Jhon Jairo Mejía Manozalba",
            "cc": "91539436"
        },
        "vehiculo": {
            "placa": "TAY 112"
        },
        "residuos": [
            {"tipo": "Biosanitarios", "cantidad": 1, "kilos": 56.00}
        ],
        "totales": {
            "cantidad": recoleccion.cantresiduo,
            "kilos": recoleccion.peso
        }
    }

    return templates.TemplateResponse("/recolecci/manifiesto.html", data)

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
            peso=totpeso[i] if totpeso and i < len(totpeso) and totpeso[i] is not None else (cantbol[i]*pesobol[i]),
            estado_id=1,
            observaciones=observ
        )
        db.add(rec)
    db.commit()
    return RedirectResponse(url="/recolecciones/", status_code=303)
