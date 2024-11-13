from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from api import models
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine
import api.schemas as schemas
import api.service.ClienteCRUD as clienteCRUD
from api.database import get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8002",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {"message": "Hello World"}


@app.get("/clientes/", response_model=list[schemas.Cliente])
def get_clientes(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    clientes = clienteCRUD.get_clientes(db,skip=skip,limit=limit)
    return clientes

@app.get("/clientes/{user_id}/",response_model=schemas.Cliente)
def get_cliente(cliente_id:int, db:Session=Depends(get_db)):
    db_user = clienteCRUD.get_user(db,user_id =cliente_id )
    if db_user is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_user

@app.post("/clientes/",response_model=schemas.Cliente)
def post_cliente(cliente:schemas.ClienteCreate, db:Session=Depends(get_db)):
    db_user = clienteCRUD.get_cliente_by_nit(db, nit=cliente.nit)
    if db_user:
        raise HTTPException(status_code=400, detail="Cliente already registered")
    return clienteCRUD.create_cliente(db=db,cliente=cliente)


if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="localhost",
                reload=True
                )
