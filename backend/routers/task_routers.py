from flask import Blueprint, request, jsonify
from backend.controllers.task_controller import create_task, edit_task, delete_task, update_task_members

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/tasks', methods=['POST'])
def create():
    data = request.json
    task = create_task(data)
    return jsonify(task)

@task_routes.route('/tasks/<int:task_id>', methods=['PUT'])
def edit(task_id):
    data = request.json
    task = edit_task(task_id, data)
    return jsonify(task)

@task_routes.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    response = delete_task(task_id)
    return jsonify(response)

@task_routes.route('/tasks/<int:task_id>/members', methods=['POST'])
def update_members(task_id):
    members = request.json.get('members')
    task = update_task_members(task_id, members)
    return jsonify(task)
