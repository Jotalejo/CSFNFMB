from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
import pdfkit
from dependencies import templates
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse
from services import RecoleccService, ClienteService

router = APIRouter(
    prefix="/certificado",
    tags=["certificado"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Inicio de la ruta para la recolección


@router.get("/{recoleccion_id}")
async def get_certificado(request: Request, recoleccion_id: int, db: Session = Depends(get_db)):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in'
    }

    template = templates.env.get_template("certificado/certificado.html")
    html = template.render({"request": request})

    pdf = pdfkit.from_string(html, False, options=options)
    headers = {'Content-Disposition': 'attachment; filename="certificado.pdf"'}

    return Response(pdf, headers=headers, media_type='application/pdf')
