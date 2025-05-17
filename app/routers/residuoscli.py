from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from services import ResiduosCliService
from schemas import ResiduosCliCreate, ResiduosCliUpdate, ResiduosCliOut
from typing import List

router = APIRouter(
    prefix="/residuoscli",
    tags=["residuoscli"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ResiduosCliOut)
def create_residuo(residuo: ResiduosCliCreate, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.create_residuo(residuo)

@router.get("/cliente/{cliente_id}", response_model=List[ResiduosCliOut])
def get_residuos(cliente_id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.get_residuos_by_cliente(cliente_id)

@router.patch("/", response_model=ResiduosCliOut)
def update_residuo(residuo: ResiduosCliUpdate, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.update_residuo(residuo)

@router.delete("/{residuo_id}", response_model=ResiduosCliOut)
def delete_residuo(residuo_id: int, db: Session = Depends(get_db)):
    service = ResiduosCliService(db)
    return service.delete_residuo(residuo_id)
