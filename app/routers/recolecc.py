from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List
from fastapi.responses import RedirectResponse
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

#@router.get("/new")
#async  def add_recolecc():
#    return "Grabando una recolección"

@router.get("/tiposresiduo/{cliente_id}", response_model=List[TipoResidOut])
def tipos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return TipoResidService(db).list_by_cliente(cliente_id)