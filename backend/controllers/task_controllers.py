from fastapi import HTTPException
from backend.db.database import SessionLocal
from backend.models.task import Task

db = SessionLocal()

def create_task(data):
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        deadline=data.get('deadline'),
        members=data.get('members')
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def edit_task(task_id, data):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in data.items():
        setattr(task, key, value)
    db.commit()
    return task

def delete_task(task_id):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}

def update_task_members(task_id, members):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.members = members
    db.commit()
    return task
