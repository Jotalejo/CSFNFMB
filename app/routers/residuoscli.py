from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from dependencies import get_db, templates
from services import ResiduosCliService, TipoResidService, ClienteService, FrecuenciaService
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

@router.get("/{id}", response_model=ResiduosCliOut)
def get_residuo(id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    residuo = service.get_residuo_by_id(id)
    if not residuo:
        raise HTTPException(status_code=404, detail="Residuo no encontrado")
    return residuo

@router.get("/cliente/{cliente_id}", response_model=List[ResiduosCliOut])
def get_residuos(cliente_id: int, request: Request, db: Session = Depends(get_db)):
    frecuenciaService = FrecuenciaService(db)
    service = ResiduosCliService(db)
    clienteService = ClienteService(db)
    residuos = service.get_residuos_by_cliente(cliente_id)
    TipoResiduo = TipoResidService(db)
    tresiduos = TipoResiduo.list_all()
    cliente = clienteService.get_cliente(cliente_id)
    url_redirect = "/residuoscli"
    action = "/residuoscli"
    frecuencias = frecuenciaService.list_by_cliente(cliente_id)
    dias_semana = [False] * 7
    if frecuencias:
        for dia in range(7):
            mask = frecuencias[0].diasem_mask
            if mask == None:
                mask = 0
            dias_semana[dia] = ((mask & (2**dia)) == (2**dia))

    frecuencia = frecuencias[0] if frecuencias else None
  


    action = f"/residuoscli/"
    method = "post" 

    return templates.TemplateResponse("/residuos/cliente.html", {"request": request, "url_redirect": url_redirect, "action": action, "method": method, "residuos": residuos, "cliente_id": cliente_id, "tresiduos": tresiduos, "cliente": cliente, "frecuencia": frecuencia, "dias_semana": dias_semana } )
                                                                 

@router.patch("/")
def update_residuo(residuo: ResiduosCliUpdate, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.update_residuo(residuo)

@router.delete("/{residuo_id}", response_model=ResiduosCliOut)
def delete_residuo(residuo_id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.delete_residuo(residuo_id)

