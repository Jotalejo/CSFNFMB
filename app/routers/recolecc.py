from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse
from services import RecoleccService

router = APIRouter(
    prefix="/recolecciones",
    tags=["recoleccion"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para la recolección
@router.get("/")
async def get_recolecc(request: Request, db:Session=Depends(get_db)):
    service = RecoleccService(db)
    recolecciones = service.get_recolecc()
    return templates.TemplateResponse("/recolecci/recolecc.html", {"request": request, "recolecciones": recolecciones} )

#@router.get("/new")
#async  def add_recolecc():
#    return "Grabando una recolección"

