# routers/tiposresid.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates, get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from services import TipoResidService, ResiduosCliService
from schemas import TipoResidCreate, TipoResidOut

router = APIRouter(
    prefix="/tiposresid",
    tags=["tipos_residuo"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# ------- Listado (JSON plano) -------
@router.get("/", response_model=List[TipoResidOut])
async def list_tiposresid(db: Session = Depends(get_db)):
    return [TipoResidOut(**row) for row in TipoResidService(db).list_all()]

# Listado para tipos de residuo por cliente
@router.get("/tipoxcliente/{cliente_id}", response_model=List[TipoResidOut])
async def list_tiposrescli(cliente_id: int, request: Request, db: Session = Depends(get_db)):
    data = TipoResidService(db).list_tiporescli(cliente_id)
    tipos_residuo = TipoResidService(db).list_all()
    return templates.TemplateResponse("/residuos/tiporesid.html", {"request": request, "data": data, "cliente_id": cliente_id, "tipos_residuo": tipos_residuo})


                      
                                                              
# DataTables-like
@router.get("/clientes/{cliente_id}/tipos_residuo/json")
async def list_tiposresid_json(cliente_id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    data = service.get_all_by_cliente(cliente_id)
    return {"data": data}

# Para selects (id, nombre)
@router.get("/options")
async def options_tiposresid(db: Session = Depends(get_db)):
    data = TipoResidService(db).list_all()
    return [{"id": x["id"], "text": x["nombre"]} for x in data]

# ------- Obtener uno -------
@router.get("/{tipores_id}", response_model=TipoResidOut)
async def get_tipores(tipores_id: int, db: Session = Depends(get_db)):
    data = TipoResidService(db).get_by_id(tipores_id)

    TipoResiduo = TipoResidService(db)
    tresiduos = TipoResidService.get_tipores()

    if not data:
        raise HTTPException(status_code=404, detail="Tipo de residuo no encontrado")
    return TipoResidOut(**data)

# ------- Crear -------
@router.post("/", response_model=TipoResidOut, status_code=201)
async def create_tipores(payload: TipoResidCreate, db: Session = Depends(get_db)):
    try:
        data = TipoResidService(db).create(payload)
        return TipoResidOut(**data)
    except IntegrityError:
        db.rollback()
        # nomtipo_tipores es UNIQUE
        raise HTTPException(status_code=409, detail="El nombre ya existe")

# ------- Actualizar -------
@router.patch("/{tipores_id}", response_model=TipoResidOut)
async def update_tipores(tipores_id: int, payload: TipoResidOut, db: Session = Depends(get_db)):
    try:
        updated = TipoResidService(db).update(tipores_id, payload)
        if not updated:
            raise HTTPException(status_code=404, detail="Tipo de residuo no encontrado")
        return TipoResidOut(**updated)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto de unicidad (nombre)")

# ------- Borrar -------
@router.delete("/{tipores_id}")
async def delete_tipores(tipores_id: int, db: Session = Depends(get_db)):
    ok = TipoResidService(db).delete(tipores_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tipo de residuo no encontrado")
    return JSONResponse({"deleted": True, "id": tipores_id})
