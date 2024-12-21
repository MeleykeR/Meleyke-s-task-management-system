from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models.task import Task
from datetime import datetime

# Create tables in the database (only once at startup)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management System!"}

# 1. Create a new task
@app.post("/tasks/")
def create_task(title: str, description: str = "", db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 2. Get all tasks
@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# 3. Get a task by ID
@app.get("/tasks/{task_id}/")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 4. Update a task by ID
@app.put("/tasks/{task_id}/")
def update_task(task_id: int, title: str = None, description: str = None, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if title:
        task.title = title
    if description:
        task.description = description
    
    db.commit()
    db.refresh(task)
    return task

# 5. Delete a task by ID
@app.delete("/tasks/{task_id}/")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} has been deleted"}

# 6. Add/Update task members
@app.post("/tasks/{task_id}/members/")
def update_task_members(task_id: int, members: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.members = members  # In this case, we're storing members as a comma-separated string
    db.commit()
    db.refresh(task)
    return task

# 7. Update the task deadline
@app.post("/tasks/{task_id}/deadline/")
def update_task_deadline(task_id: int, deadline: datetime, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.deadline = deadline
    db.commit()
    db.refresh(task)
    return task
