from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db
from schemas import ClienteCreate, Cliente
from services import ClienteService, CiudadService
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse

# Ruta primaria para el cliente potencial
router = APIRouter(
    prefix="/clienpot",
    tags=["clienpot"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para el cliente
@router.get("/clienpot")
async def get_clients(request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    clientes = service.get_clientes()
    return templates.TemplateResponse("/crm/clicrm.html", {"request": request, "clientes": clientes} )

