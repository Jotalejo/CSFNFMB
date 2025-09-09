from routers.clienpot import router as clienpot_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from dependencies import get_db
from routers import clients, residuoscli, recolecc, usuarios, crm, tiposresid

from dependencies import templates
from jose import jwt, JWTError
# Load environment
from dotenv import load_dotenv
import os
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)

# Importar la ruta de cliente
app = FastAPI(debug=True, redirect_slashes=False)
#app = FastAPI(redirect_slashes=False)
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
                   "*"])  # O tu dominio público
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(clients.router)
app.include_router(residuoscli.router)
app.include_router(recolecc.router)
app.include_router(usuarios.router)
app.include_router(crm.router)
app.include_router(tiposresid.router)

# Clientes potenciales
app.include_router(clienpot_router)


# Rutas públicas (exactas) y prefijos (estáticos)
PUBLIC_EXACT = {"/", "/usuarios/login", "/usuarios/reset-password", "/usuarios/logout", "/favicon.ico"}
PUBLIC_PREFIXES = ("/static",)  # agrega otros prefijos si hace falta

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    path = request.url.path
    try:
        # Público por path exacto o prefijo (estáticos)
        if path in PUBLIC_EXACT or any(path.startswith(p) for p in PUBLIC_PREFIXES):
            return await call_next(request)

        # Protegido: requiere cookie
        token = request.cookies.get("access_token")
        if not token:
            logging.info("No token found, redirecting to /usuarios/login")
            return RedirectResponse(url="/usuarios/login", status_code=303)

        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await call_next(request)

    except JWTError:
        logging.info("Invalid token, redirecting to /usuarios/login")
        return RedirectResponse(url="/usuarios/login", status_code=303)
    except Exception as e:
        logging.exception("Error in middleware")
        # devuelvo 500 con texto simple para que se vea algo si el error fuera aquí
        return PlainTextResponse(f"Middleware error: {e}", status_code=500)

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    # Si esto falla, es la plantilla. Debajo te dejo un endpoint de diagnóstico.
    return templates.TemplateResponse("index1.html", {"request": request, "name": "Gresab"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
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

@app.get("/exit", response_class=HTMLResponse)
async def recolecc(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request, "lista": [], "name": "Gresab"})

@app.get("/__ping")
async def ping():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
