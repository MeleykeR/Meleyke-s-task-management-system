from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
from backend.models.task import Task, tasks

task_routes = Blueprint("tasks", __name__)
api = Api(task_routes, doc="/docs", title="Task Management API", description="API for managing tasks")

# Define the task model for Swagger documentation
task_model = api.model("Task", {
    "id": fields.Integer(description="The unique identifier of the task"),
    "title": fields.String(required=True, description="The title of the task"),
    "description": fields.String(required=True, description="The description of the task"),
    "deadline": fields.String(description="The deadline of the task"),
    "members": fields.List(fields.String, description="List of task members"),
})

# Task CRUD routes
@api.route("/tasks")
class TaskList(Resource):
    @api.doc("list_tasks")
    @api.marshal_list_with(task_model)
    def get(self):
        """List all tasks"""
        return tasks

    @api.expect(task_model)
    @api.doc("create_task")
    def post(self):
        """Create a new task"""
        new_task = api.payload
        new_task["id"] = len(tasks) + 1
        tasks.append(new_task)
        return {"message": "Task created successfully", "task": new_task}, 201

@api.route("/tasks/<int:id>")
@api.param("id", "The task identifier")
class Task(Resource):
    @api.doc("get_task")
    @api.marshal_with(task_model)
    def get(self, id):
        """Get a task by ID"""
        task = next((task for task in tasks if task["id"] == id), None)
        if not task:
            api.abort(404, f"Task {id} not found")
        return task

    @api.doc("delete_task")
    def delete(self, id):
        """Delete a task by ID"""
        global tasks
        tasks = [task for task in tasks if task["id"] != id]
        return {"message": f"Task {id} deleted successfully"}

    @api.expect(task_model)
    @api.doc("update_task")
    def put(self, id):
        """Update a task by ID"""
        task = next((task for task in tasks if task["id"] == id), None)
        if not task:
            api.abort(404, f"Task {id} not found")
        task.update(api.payload)
        return {"message": f"Task {id} updated successfully", "task": task}
