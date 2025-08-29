from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from dependencies import templates, get_db
from services import ClipotService

router = APIRouter(
    prefix="/crm",
    tags=["crm"],
    dependencies=[Depends(get_db)],
)

@router.get("")
async def crm_home(request: Request, db: Session = Depends(get_db)):
    # Si quieres precargar algo, p.ej. conteos, hazlo aquí
    return templates.TemplateResponse("/crm/clicrm.html", {"request": request})


