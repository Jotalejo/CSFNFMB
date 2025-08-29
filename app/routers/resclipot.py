# routers/resclipot.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Dict, Any
from dependencies import get_db, templates

from services import resclipot
from services.resclipot import ResCliPotService
from schemas.Resclipot import ResiduosCliCreate, ResiduosCliUpdate

router = APIRouter(
    prefix="/resclipot",
    tags=["residuos_potenciales"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# ---------- JSON para DataTable por cliente POT ----------
@router.get("/clipot/{clipot_id}/json")
async def resclipot_by_clipot_json(clipot_id: int, db: Session = Depends(get_db)):
    data = ResCliPotService(db).list_by_clipot(clipot_id)
    return {"data": data}

# ---------- Modal HTML (se inyecta en #MdlGestRescli) ----------
@router.get("/clipot/{clipot_id}")
async def resclipot_modal_clipot(clipot_id: int, request: Request):
    return templates.TemplateResponse(
        "/resclipot/edit.html",  # mueve el template aquí
        {"request": request, "clipot_id": clipot_id}
    )

# ---------- Obtener un residuo POT por id (JSON, para precarga) ----------
@router.get("/{resid_id}")
async def resclipot_get(resid_id: int, db: Session = Depends(get_db)):
    data = ResCliPotService(db).get_by_id(resid_id)
    if not data:
        raise HTTPException(status_code=404, detail="Residuo potencial no encontrado")
    return data

# ---------- Guardar desde FORM del modal (crear/actualizar) ----------
@router.post("/form")
async def resclipot_form_submit(
    resid_id: Annotated[Optional[int], Form(None)] = None,
    ccliente: Annotated[int, Form()] = None,
    tresiduo: Annotated[int, Form()] = None,
    cantresiduo: Annotated[Optional[float], Form(None)] = None,
    pesopromres: Annotated[Optional[float], Form(None)] = None,
    segregares: Annotated[Optional[str], Form(None)] = None,
    numbolsas: Annotated[Optional[int], Form(None)] = None,
    observaciones: Annotated[Optional[str], Form(None)] = None,
    db: Session = Depends(get_db),
):
    payload: Dict[str, Any] = {
        "ccliente": ccliente,
        "tresiduo": tresiduo,
        "cantresiduo": cantresiduo,
        "pesopromres": pesopromres,
        "segregares": segregares,
        "numbolsas": numbolsas,
        "observaciones": observaciones,
    }
    service = ResCliPotService(db)
    if resid_id:
        updated = service.update_from_form(resid_id, payload)
        if not updated:
            raise HTTPException(status_code=404, detail="Residuo potencial no encontrado")
    else:
        service.create_from_form(payload)

    return RedirectResponse(url=f"/resclipot/clipot/{ccliente}/json", status_code=303)

# ---------- CRUD JSON puro ----------
@router.post("/")
async def resclipot_create_json(payload: ResiduosCliCreate, db: Session = Depends(get_db)):
    return ResCliPotService(db).create(payload)

@router.patch("/{resid_id}")
async def resclipot_update_json(resid_id: int, payload: ResiduosCliUpdate, db: Session = Depends(get_db)):
    updated = ResCliPotService(db).update(resid_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Residuo potencial no encontrado")
    return updated

@router.delete("/{resid_id}")
async def resclipot_delete(resid_id: int, db: Session = Depends(get_db)):
    ok = ResCliPotService(db).delete(resid_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Residuo potencial no encontrado")
    return {"deleted": True, "id": resid_id}
