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

router = APIRouter(
    prefix="/recolecciones",
    tags=["recoleccion"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para la recolección
@router.get("/")
async def get_recolecc(request: Request, db:Session=Depends(get_db)):
    service = RecoleccService(db)
    clientService =  ClienteService(db)
    recolecciones = service.get_recolecc()
    clientes = clientService.get_clientes()
    return templates.TemplateResponse("/recolecci/recolecc.html", {"request": request, "recolecciones": recolecciones, "clientes": clientes} )

@router.get("/detalle/{rec_id}", response_class=HTMLResponse)
def detalle_recoleccion(rec_id: int, request: Request, db: Session = Depends(get_db)):
    service = RecoleccService(db)
    r = service.get_recolecc_by_id(rec_id)
    if not r:
        raise HTTPException(status_code=404, detail="Recolección no encontrada")
    # Renderiza un parcial (solo el cuerpo del modal)
    return templates.TemplateResponse("recolecci/_detalle_modal.html", {"request": request, "r": r})

#@router.get("/new")
#async  def add_recolecc():
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
        #hora=hora_obj, # type: ignore
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
