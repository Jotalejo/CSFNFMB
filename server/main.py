from fastapi import FastAPI, Depends, HTTPException,Request,Response
from fastapi.staticfiles import StaticFiles
import uvicorn
from api import models
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine
import api.schemas as schemas
import api.service.ClienteCRUD as clienteCRUD
from api.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse 
import pathlib

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://127.0.0.1:8000"
    "http://localhost:8000"
    "http://localhost:8002",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

client_dir = pathlib.Path('dist')

@app.get('/')
def home():
    return FileResponse('dist/index.html')

@app.get("/api/clientes", response_model=list[schemas.Cliente])
def get_clientes(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    clientes = clienteCRUD.get_clientes(db,skip=skip,limit=limit)
    return clientes

@app.get("/api/clientes/{id}",response_model=schemas.Cliente)
def get_cliente(id:int, db:Session=Depends(get_db)):
    db_user = clienteCRUD.get_cliente(db,cliente_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_user

@app.post("/api/clientes/",response_model=schemas.Cliente)
def post_cliente(cliente:schemas.ClienteCreate, db:Session=Depends(get_db)):
    db_user = clienteCRUD.get_cliente_by_nit(db, nit=cliente.nit)
    if db_user:
        raise HTTPException(status_code=400, detail="Cliente already registered")
    return clienteCRUD.create_cliente(db=db,cliente=cliente)

@app.patch("/api/clientes/{id}",response_model=schemas.Cliente)
def post_cliente(cliente:schemas.ClienteCreate, db:Session=Depends(get_db)):
    db_user = clienteCRUD.get_cliente_by_nit(db, nit=cliente.nit)
    if db_user:
        raise HTTPException(status_code=400, detail="Cliente already registered")
    return clienteCRUD.update_cliente(db=db,cliente=cliente)

@app.get('/{path:path}')
async def handle_catch_all(request: Request, path):
    if path and path != "/":
        disk_path = client_dir.joinpath(path)
        if disk_path.exists():
            content = disk_path.read_bytes()
            content_type = "text/html"
            
            # Set correct MIME types for different file extensions
            if path.endswith(".js"):
                content_type = "application/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".svg"):
                content_type = "image/svg+xml"
            
            return Response(content, 200, media_type=content_type)
        else:
            if disk_path.is_file():
                raise fastapi.exceptions.HTTPException(404)

    return FileResponse('dist/index.html')




if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="localhost",
                reload=True
                )
