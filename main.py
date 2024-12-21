from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models.task import Task

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management System!"}

@app.post("/tasks/")
def create_task(title: str, description: str = "", db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
