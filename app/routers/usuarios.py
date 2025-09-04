import email
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from services import AuthService
from dependencies import templates, get_db
from schemas import RequestDetails, TokenSchema, ResetPassword
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import get_settings, Settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Ruta primaria para los usuarios
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", response_class=templates.TemplateResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("/usuarios/login.html", {"request": request})


@router.post("/login", response_model=TokenSchema)
async def login(request: Request,
                data: Annotated[RequestDetails, Form()],
                db: Session = Depends(get_db),
                settings: Settings = Depends(get_settings)):

    username = data.email
    password = data.password

    # Aquí se debería implementar la lógica de autenticación
    if not username or not password:
        raise HTTPException(
            status_code=400, detail="Username and password are required")

    authService = AuthService(db)

    user = authService.authenticate_user(username, password)

    if not user:
        return templates.TemplateResponse("/usuarios/login.html", {"request": request, "error": "Invalid credentials"})

    token_data = {"sub": username,
                  "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                  }
    token = jwt.encode(token_data, settings.SECRET_KEY,
                       algorithm=settings.ALGORITHM)
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


async def send_reset_email(email: str, reset_link: str, settings: Settings):

    message = MessageSchema(
        subject="Restablecer contraseña",
        recipients=[email],
        body=f"Haz clic aquí para restablecer tu contraseña: {reset_link}",
        subtype="plain"
    )
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=settings.MAIL_TLS,
        MAIL_SSL_TLS=settings.MAIL_SSL
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@router.get("/reset-password", response_class=templates.TemplateResponse, name="reset_password_form")
async def reset_password_form(request: Request, db: Session = Depends(get_db), token: str = None):
    if not token:
        return templates.TemplateResponse("/usuarios/reset_password.html", {"request": request})
    authService = AuthService(db)
    email = authService.verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    new_password = authService.generate_password()
    authService.update_password(email, new_password)
    return templates.TemplateResponse(
        "/usuarios/reset_password_success.html",
        {"request": request, "email": email, "new_password": new_password}
    )


@router.post("/reset-password", response_class=templates.TemplateResponse)
async def reset_password(request: Request,
                         data: Annotated[ResetPassword, Form()],
                         db: Session = Depends(get_db),
                         settings: Settings = Depends(get_settings)
                         ):

    if not data.email:
        raise HTTPException(status_code=400, detail="Email is required")

    authService = AuthService(db)

    user = authService.get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = authService.create_reset_token(data.email)
    reset_path = request.url_for(
        "reset_password_form").include_query_params(token=token)

    await send_reset_email(data.email, reset_path, settings)
    return templates.TemplateResponse("/usuarios/reset_password_sent.html", {"request": request})

# routers/usuarios.py
# from fastapi import APIRouter
# from fastapi.responses import RedirectResponse

# router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/logout")
async def logout():
    resp = RedirectResponse(url="/", status_code=303)  # o "/usuarios/login"
    # Usa el mismo path/domain que usaste al setear la cookie
    resp.delete_cookie(key="access_token", path="/")
    return resp

