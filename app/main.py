from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dependencies import get_db
from routers import clients, residuoscli, recolecc
from dependencies import templates

# Importar la ruta de cliente
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(clients.router)
app.include_router(residuoscli.router)
app.include_router(recolecc.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "World"})

@app.get("/fuente", response_class=HTMLResponse)
async def fuente_generadora(request: Request):
    return templates.TemplateResponse("fuente_generadora.html", {"request": request, "lista": [], "name": "World"})

@app.get("/validation", response_class=HTMLResponse)
async def validation(request: Request):
    return templates.TemplateResponse("form-validation.html", {"request": request, "lista": [], "name": "World"})

@app.get("/recolecc", response_class=HTMLResponse)
async def recolecc(request: Request):
    return templates.TemplateResponse("recolecc.html", {"request": request, "lista": [], "name": "World"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)