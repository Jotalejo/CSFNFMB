from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db
from schemas import ClienteCreate, Cliente
from services import ClienteService, CiudadService, TipoResidService
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse

# Ruta primaria para el cliente
router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para el cliente
@router.get("/")
async def get_clients(request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    clientes = service.get_clientes()
    return templates.TemplateResponse("/clientes/search.html", {"request": request, "clientes": clientes} )

@router.get("/json")
async def get_clients_json(db:Session=Depends(get_db)):
    service = ClienteService(db)
    clientes = service.get_clientes()
    return {"data":clientes}

# Boton que había de buscar cliente
@router.post("/search")
async def search_clients(request: Request, nit: Annotated[str, Form()], db:Session=Depends(get_db)):
    service = ClienteService(db)
    cliente = service.get_cliente_by_nit(nit)
    action = "/clientes/"
    method = "post"

    ciudadesService = CiudadService(db)
    ciudades = ciudadesService.get_ciudades()

    if (cliente != None):
        action =  "/clientes/{}".format(cliente.id)
        method = "patch"
    return templates.TemplateResponse("/clientes/edit.html", {"request": request, "cliente": cliente, "action": action, "method": method, "ciudades": ciudades} )

# Crear Cliente
@router.post("/")
async def create_client(client: ClienteCreate,  db:Session=Depends(get_db)):
    service = ClienteService(db)
    dbCliente = service.create_cliente(client)
    return dbCliente

# Crea Cliente Mandar al formulario
@router.get("/nuevo")
async def creafor_client(request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    action = "/clientes/"
    method = "post"

    ciudadesService = CiudadService(db)
    ciudades = ciudadesService.get_ciudades()

    url_redirect = router.url_path_for("get_clients")

    return templates.TemplateResponse("/clientes/edit.html", {"request": request,"cliente": None, "action": action, "method": method, "ciudades": ciudades, "url_redirect": url_redirect} )

# Actualizar Cliente
@router.patch("/{cliente_id}")
async def update_client(cliente_id: int, client: Cliente,  db:Session=Depends(get_db)):
    service = ClienteService(db)
    dbCliente = service.update_cliente(client)
    return dbCliente

# Trae un Cliente
@router.get("/{cliente_id}")
async def get_client(cliente_id: int, request: Request, db:Session=Depends(get_db)):
    service = ClienteService(db)
    ciudadesService = CiudadService(db)

    cliente = service.get_cliente(cliente_id)
    action = "/clientes/{}".format(cliente.id)
    method = "patch"

    ciudades = ciudadesService.get_ciudades()
    url_redirect = router.url_path_for("get_clients")

    return templates.TemplateResponse("/clientes/edit.html", {"request": request,
                                                              "cliente": cliente,
                                                              "action": action,
                                                              "method": method,
                                                              "ciudades": ciudades,
                                                              "url_redirect": url_redirect})

