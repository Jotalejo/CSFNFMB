from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from dependencies import get_db, templates
from services import ResiduosCliService, TipoResidService
from schemas import ResiduosCliCreate, ResiduosCliUpdate, ResiduosCliOut
from typing import List

router = APIRouter(
    prefix="/residuoscli",
    tags=["residuoscli"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_residuo(residuo: ResiduosCliCreate, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.create_residuo(residuo)

@router.get("/cliente/{cliente_id}", response_model=List[ResiduosCliOut])
def get_residuos(cliente_id: int, request: Request, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    residuos = service.get_residuos_by_cliente(cliente_id)
    TipoResiduo = TipoResidService(db)
    tresiduos = TipoResiduo.list_all()
    url_redirect = "/residuoscli"
    action = "/residuoscli"
    method = "post"

    return templates.TemplateResponse("/residuos/cliente.html", {"request": request, "url_redirect": url_redirect, "action": action, "method": method, "residuos": residuos, "cliente_id": cliente_id, "tresiduos": tresiduos} )
                                                                 

@router.patch("/")
def update_residuo(residuo: ResiduosCliUpdate, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.update_residuo(residuo)

@router.delete("/{residuo_id}", response_model=ResiduosCliOut)
def delete_residuo(residuo_id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.delete_residuo(residuo_id)

