from backend.db.database import SessionLocal
from backend.models.task import Task

def populate_db():
    """Add dummy data to the database."""
    db = SessionLocal()

    # Check if the database already has data
    if db.query(Task).count() > 0:
        print("Database already populated.")
        db.close()
        return

    # Add sample tasks
    tasks = [
        Task(
            title="Complete Project Report",
            description="Finish the report by Monday.",
            deadline="2024-12-25",
            members=["Alice", "Bob"],
        ),
        Task(
            title="Plan Team Meeting",
            description="Organize the weekly team meeting.",
            deadline="2024-12-22",
            members=["Charlie"],
        ),
        Task(
            title="Code Review",
            description="Review pull requests for the new feature.",
            deadline="2024-12-23",
            members=["Alice", "David"],
        ),
    ]

    # Insert tasks into the database
    db.add_all(tasks)
    db.commit()
    print("Dummy data added to the database.")
    db.close()

if __name__ == "__main__":
    populate_db()
