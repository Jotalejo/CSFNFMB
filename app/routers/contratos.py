from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from dependencies import templates, get_db
from schemas.Contrato import ContratoCreate
from services.contrato_service import ContratoService

router = APIRouter(
    prefix="/contratos",
    tags=["contratos"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

TEMPLATE_DOCX = "static/plantillas/contrato_template_gresab.docx"
OUT_DIR = "static/contratos"

@router.get("/cliente/{cliente_id}")
async def modal_contrato(cliente_id: int, request: Request):
    return templates.TemplateResponse(
        "/contratos/mdl-contrato.html",
        {
            "request": request,
            "cliente_id": cliente_id
        }
    )

@router.post("/cliente/{cliente_id}/generar")
async def generar_contrato(
    cliente_id: int,
    fecha_inicio: str = Form(...),
    lugar_ejecucion: str = Form(...),
    rep_nombre: str = Form(...),
    rep_cc: str = Form(...),
    rep_exp_lugar: str = Form(...),
    fecha_firma: str = Form(...),
    mes_actual: str = Form(""),
    db: Session = Depends(get_db),
):
    payload = ContratoCreate(
        fecha_inicio=fecha_inicio,
        lugar_ejecucion=lugar_ejecucion,
        rep_nombre=rep_nombre,
        rep_cc=rep_cc,
        rep_exp_lugar=rep_exp_lugar,
        fecha_firma=fecha_firma,
        mes_actual=mes_actual,
    )

    service = ContratoService(db, TEMPLATE_DOCX, OUT_DIR)
    contrato = service.crear_y_generar_pdf(cliente_id, payload)

    if not contrato:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return FileResponse(
        path=contrato.pdf_path,
        media_type="application/pdf",
        filename=f"Contrato_{cliente_id}.pdf"
    )

@router.get("/cliente/{cliente_id}/historial")
async def historial_contratos(cliente_id: int, request: Request, db: Session = Depends(get_db)):
    service = ContratoService(db, TEMPLATE_DOCX, OUT_DIR)
    contratos = service.get_contratos_by_cliente(cliente_id)

    return templates.TemplateResponse(
        "/contratos/historial.html",
        {
            "request": request,
            "cliente_id": cliente_id,
            "contratos": contratos
        }
    )

@router.get("/{contrato_id}/descargar")
async def descargar_contrato(contrato_id: int, db: Session = Depends(get_db)):
    service = ContratoService(db, TEMPLATE_DOCX, OUT_DIR)
    contrato = service.get_contrato(contrato_id)

    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    return FileResponse(
        path=contrato.pdf_path,
        media_type="application/pdf",
        filename=f"Contrato_{contrato.id}.pdf"
    )