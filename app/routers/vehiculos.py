# routers/vehiculos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from services.vehiculo_service import VehiculoService

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])

@router.get("/options")
def vehiculos_options(db: Session = Depends(get_db)):
    return VehiculoService(db).options()
