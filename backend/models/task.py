from datetime import datetime

class Task:
    def __init__(self, id, title, description, deadline, members):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.members = members

# Sample tasks (in-memory for demonstration)
tasks = [
    Task(1, "Complete Project Report", "Finish the report by Monday.", "2024-12-25", ["Alice", "Bob"]),
    Task(2, "Plan Team Meeting", "Organize the weekly team meeting.", "2024-12-22", ["Charlie"]),
    Task(3, "Code Review", "Review pull requests for the new feature.", "2024-12-23", ["Alice", "David"]),
]
