import email
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from services import AuthService
from dependencies import templates, get_db
from schemas import RequestDetails, TokenSchema, ResetPassword, OTPSetupResponse, OTPVerifyRequest
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import RedirectResponse, JSONResponse
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

    # Verificar si el usuario tiene OTP habilitado
    if user.otp_enabled:
        # Redirigir a la página de verificación OTP
        # Guardar datos temporales en sesión o cookie temporal
        temp_token_data = {
            "sub": username,
            # Token temporal de 5 minutos
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "temp": True
        }
        temp_token = jwt.encode(
            temp_token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        response = RedirectResponse(
            url="/usuarios/otp/verify-page", status_code=302)
        response.set_cookie(key="temp_token", value=temp_token,
                            httponly=True, max_age=300)
        return response

    # Login normal sin OTP
    token_data = {"sub": username,
                  "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                  "otp_verified": False
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


# ============= ENDPOINTS OTP =============

@router.post("/otp/setup", response_model=OTPSetupResponse)
async def setup_otp(request: Request, db: Session = Depends(get_db)):
    """Genera el QR code para configurar Google Authenticator"""
    # Obtener el email del usuario autenticado desde el token
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[
                             get_settings().ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    authService = AuthService(db)
    otp_data = authService.setup_otp_for_user(email)

    if not otp_data:
        raise HTTPException(status_code=404, detail="User not found")

    return OTPSetupResponse(
        secret=otp_data["secret"],
        qr_code_url=otp_data["qr_code_url"]
    )


@router.get("/otp/setup-page", response_class=templates.TemplateResponse)
async def otp_setup_page(request: Request):
    """Página HTML para configurar OTP"""
    return templates.TemplateResponse("/usuarios/otp_setup.html", {"request": request})


@router.post("/otp/enable")
async def enable_otp(request: Request, data: OTPVerifyRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    """Habilita OTP después de verificar el código del usuario"""
    # Obtener el email del usuario autenticado desde el token
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    authService = AuthService(db)

    if authService.enable_otp_for_user(email, data.otp_code):
        return {"message": "OTP enabled successfully"}

    raise HTTPException(status_code=400, detail="Invalid OTP code")


@router.post("/otp/disable")
async def disable_otp(request: Request, db: Session = Depends(get_db)):
    """Deshabilita OTP para el usuario"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[
                             get_settings().ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    authService = AuthService(db)

    if authService.disable_otp_for_user(email):
        return {"message": "OTP disabled successfully"}

    raise HTTPException(status_code=400, detail="Failed to disable OTP")


@router.post("/otp/verify")
async def verify_otp(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verifica un código OTP (usado durante el login)"""
    authService = AuthService(db)

    if authService.verify_otp(data.email, data.otp_code):
        return {"message": "OTP verified successfully"}

    raise HTTPException(status_code=400, detail="Invalid OTP code")


@router.get("/otp/verify-page", response_class=templates.TemplateResponse)
async def otp_verify_page(request: Request):
    """Página HTML para verificar el código OTP"""
    return templates.TemplateResponse("/usuarios/otp_verify.html", {"request": request})


@router.post("/otp/verify-login")
async def verify_otp_login(
    request: Request,
    otp_code: Annotated[str, Form()],
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    """Verifica el código OTP después del login"""
    temp_token = request.cookies.get("temp_token")

    if not temp_token:
        return templates.TemplateResponse("/usuarios/login.html", {
            "request": request,
            "error": "Session expired. Please login again."
        })

    try:
        payload = jwt.decode(temp_token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if not payload.get("temp"):
            raise HTTPException(status_code=400, detail="Invalid token")

        authService = AuthService(db)

        if authService.verify_otp(email, otp_code):
            # Crear token definitivo con OTP verificado
            token_data = {
                "sub": email,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "otp_verified": True
            }
            token = jwt.encode(token_data, settings.SECRET_KEY,
                               algorithm=settings.ALGORITHM)

            response = RedirectResponse(url="/dashboard", status_code=302)
            response.delete_cookie(key="temp_token")
            response.set_cookie(key="access_token", value=token, httponly=True)
            return response
        else:
            return templates.TemplateResponse("/usuarios/otp_verify.html", {
                "request": request,
                "error": "Invalid OTP code. Please try again."
            })

    except jwt.JWTError:
        return templates.TemplateResponse("/usuarios/login.html", {
            "request": request,
            "error": "Session expired. Please login again."
        })
