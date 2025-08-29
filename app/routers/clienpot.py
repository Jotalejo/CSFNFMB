# routers/clienpot.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Annotated
from dependencies import get_db, templates

from services.clienpot import ClipotService
from schemas.Clienpot import CliPotCreate, Clipot as ClipotSchema

router = APIRouter(
    prefix="/clienpot",
    tags=["clienpot"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para el cliente
@router.get("/")
async def get_clienpot(request: Request, db:Session=Depends(get_db)):
    service = ClipotService(db)
    #clienpot = service.get_clientes()
    return templates.TemplateResponse("/crm/clicrm.html", {"request": request} )

# -------- JSON para DataTable (wizard CRM) --------
@router.get("/json")
async def clienpot_json(db: Session = Depends(get_db)):
    data = ClipotService(db).get_clipots()
    return {"data": data}

# -------- Crear (JSON) --------
@router.post("/")
async def clienpot_create(payload: CliPotCreate, db: Session = Depends(get_db)):
    try:
        created = ClipotService(db).create_clipot(payload)
        return created
    except IntegrityError as e:
        # Duplicado de NIT o razonsoc
        raise HTTPException(status_code=409, detail="Razon social o NIT ya existen") from e

# -------- Obtener uno (JSON) --------
@router.get("/{clipot_id}/json")
async def clienpot_get_json(clipot_id: int, db: Session = Depends(get_db)):
    item = ClipotService(db).get_clipot(clipot_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cliente potencial no encontrado")
    return item

# -------- Actualizar (JSON) --------
@router.patch("/{clipot_id}")
async def clienpot_update(clipot_id: int, payload: ClipotSchema, db: Session = Depends(get_db)):
    try:
        updated = ClipotService(db).update_clipot(clipot_id, payload)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Razon social o NIT ya existen") from e
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente potencial no encontrado")
    return updated

# -------- Borrar (JSON) --------
@router.delete("/{clipot_id}")
async def clienpot_delete(clipot_id: int, db: Session = Depends(get_db)):
    ok = ClipotService(db).delete_clipot(clipot_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cliente potencial no encontrado")
    return {"deleted": True, "id": clipot_id}

# ============================================================
# (Opcional) Vistas HTML para crear/editar fuera del wizard
# ============================================================

@router.get("/nuevo")
async def clienpot_new_view(request: Request):
    action = "/clienpot/"
    method = "post"
    return templates.TemplateResponse("/clienpot/edit.html", {
        "request": request, "clipot": None, "action": action, "method": method
    })

@router.get("/{clipot_id}")
async def clienpot_edit_view(clipot_id: int, request: Request, db: Session = Depends(get_db)):
    item = ClipotService(db).get_clipot(clipot_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cliente potencial no encontrado")
    action = f"/clienpot/{clipot_id}"
    method = "patch"
    return templates.TemplateResponse("/clienpot/edit.html", {
        "request": request, "clipot": item, "action": action, "method": method
    })
