from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dependencies import get_db
from routers import clients, residuoscli, recolecc, usuarios, crm
from dependencies import templates
from jose import jwt, JWTError
# Load environment
from dotenv import load_dotenv
import os
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)

# Importar la ruta de cliente
app = FastAPI(redirect_slashes=False)
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
                   "*"])  # O tu dominio público
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(clients.router)
app.include_router(residuoscli.router)
app.include_router(recolecc.router)
app.include_router(usuarios.router)
app.include_router(crm.router)

# Clientes potenciales
from routers.clienpot import router as clienpot_router
app.include_router(clienpot_router)

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    # Rutas públicas que no requieren autenticación
    public_paths = ["/usuarios/login",
                    "/usuarios/reset-password",
                    "/static", "/favicon.ico"]

    # Permitir acceso a rutas públicas
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Verificar token en cookie
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/usuarios/login")

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return RedirectResponse(url="/usuarios/login")

    # Si el token es válido, continuar con la petición
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Gresab"})


@app.get("/fuente", response_class=HTMLResponse)
async def fuente_generadora(request: Request):
    return templates.TemplateResponse("fuente_generadora.html", {"request": request, "lista": [], "name": "Gresab"})


@app.get("/validation", response_class=HTMLResponse)
async def validation(request: Request):
    return templates.TemplateResponse("form-validation.html", {"request": request, "lista": [], "name": "Gresab"})


@app.get("/recolecc", response_class=HTMLResponse)
async def recolecc(request: Request):
    return templates.TemplateResponse("recolecc.html", {"request": request, "lista": [], "name": "Gresab"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
