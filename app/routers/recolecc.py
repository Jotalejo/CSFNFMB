from fastapi import APIRouter, Depends, HTTPException, Request, Form
from dependencies import templates
from dependencies import get_db


from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse

@recolecc.route("/rootrclt")
def homer():
    return "Hello world 2"

@recolecc.route("/new")
def add_recolecc():
    return "Grabando una recolección"

# Ruta primaria para las recolecciones
router = APIRouter(
    prefix="/recolecciones",
    tags=["recolecciones"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para la recolección
@router.get("/")
async def get_recolecc(request: Request, db:Session=Depends(get_db)):
    service = RecoleccService(db)
    recoleccion = service.get_recolecc()
    return templates.TemplateResponse("/recolecci/recolecc.html", {"request": request, "recoleccion": recoleccion} )

