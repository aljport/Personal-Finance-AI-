import uvicorn 
from fastapi import FastAPI, Depends, HTTPException
import models
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated

app =  FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware (
    CORSMiddleware,
    allow_origins=origins,

)

class CalculateBase(BaseModel):
    goal: int 
    years: float
    category: str

class CalculateModel(CalculateBase):
    class Config:
        orm_mode = True
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine)

@app.post("/calculations/", response_model=CalculateModel)
async def create_calculation(calculate: CalculateBase, db: db_dependency):
    db_calulate = models.Calculate(**calculate.dict())
    db.add(db_calulate)
    db.commit()
    db.refresh(db_calulate)
    return db_calulate

@app.get('/')
def index():
    return {'message' : 'Hi there'}

@app.get('/Welcome')
def get_name(name: str):
    return {'Personal finance AI'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)