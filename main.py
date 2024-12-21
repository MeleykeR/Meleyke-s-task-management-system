from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
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

@app.post("/populate_dummy_data", tags=["Database Management"], summary="Populate Dummy Data")
def populate_dummy_data(db: Session = Depends(get_db)):
    """
    Populate the database with dummy tasks for testing purposes.
    """
    dummy_tasks = [
        Task(title="Task 1", description="Description 1", members="Alice,Bob", deadline=datetime(2024, 12, 25)),
        Task(title="Task 2", description="Description 2", members="Charlie", deadline=datetime(2024, 12, 31)),
    ]
    db.add_all(dummy_tasks)
    db.commit()
    return {"message": "Dummy data has been populated."}

@app.post("/reset_database", tags=["Database Management"], summary="Reset Database")
def reset_database(db: Session = Depends(get_db)):
    """
    Reset the database by deleting all tasks.
    """
    db.query(Task).delete()
    db.commit()
    return {"message": "Database has been reset."}

@app.get("/tasks/", tags=["Task Management"], summary="Get All Tasks")
def get_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks from the database.
    """
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}/", tags=["Task Management"], summary="Get Task by ID")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single task by its ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}/", tags=["Task Management"], summary="Update Task by ID")
def update_task(task_id: int, title: str = None, description: str = None, db: Session = Depends(get_db)):
    """
    Update a task's title or description by ID.
    """
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

@app.delete("/tasks/{task_id}/", tags=["Task Management"], summary="Delete Task by ID")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} has been deleted"}

@app.post("/tasks/{task_id}/members/", tags=["Task Members"], summary="Update Task Members")
def update_task_members(task_id: int, members: str, db: Session = Depends(get_db)):
    """
    Add or update task members by ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.members = members
    db.commit()
    db.refresh(task)
    return task

@app.post("/tasks/{task_id}/deadline/", tags=["Task Deadlines"], summary="Update Task Deadline")
def update_task_deadline(task_id: int, deadline: datetime, db: Session = Depends(get_db)):
    """
    Update a task's deadline by ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.deadline = deadline
    db.commit()
    db.refresh(task)
    return task
