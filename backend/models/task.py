from sqlalchemy import Column, Integer, String, Text, Date, JSON
from backend.db.database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(Date, nullable=True)
    members = Column(JSON, nullable=True)  # Store members as a JSON array
