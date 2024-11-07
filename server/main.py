from fastapi import FastAPI
import uvicorn
from app import model
from app.database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="localhost",
                reload=True
                )
