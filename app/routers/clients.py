from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db
from schemas import ClienteCreate, Cliente
from services import ClienteService
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_clients(request: Request):
    return templates.TemplateResponse("/clientes/search.html", {"request": request})

@router.post("/search")
async def search_clients(request: Request, nit: Annotated[str, Form()], db:Session=Depends(get_db)):
    service = ClienteService(db)
    cliente = service.get_cliente_by_nit(nit)
    action = "/clientes"
    method = "post"

    if (cliente != None):
        action =  "/clientes/{}".format(cliente.id)
        method = "patch"
    return templates.TemplateResponse("/clientes/edit.html", {"request": request, "cliente": cliente, "action": action, "method": method} )

@router.post("/")
async def create_client(client: ClienteCreate,  db:Session=Depends(get_db)):
    service = ClienteService(db)
    dbCliente = service.create_cliente(client)
    return dbCliente 

@router.get("/{cliente_id}")
async def get_client(cliente_id: int, request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    cliente = service.get_cliente(cliente_id)
    action = "/clientes/{}".format(cliente.id)
    method = "patch"
    return templates.TemplateResponse("/clientes/edit.html", {"request": request, "cliente": cliente, "action": action, "method": method} )

@router.patch("/{cliente_id}")
async def update_client(cliente_id: int, client: Cliente, request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    dbCliente = service.update_cliente(client)
    return dbCliente
