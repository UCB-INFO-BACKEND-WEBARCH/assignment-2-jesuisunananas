from flask import Blueprint, jsonify, request
from models import db, TaskModel, CategoryModel
from schemas import TaskSchema
from marshmallow import ValidationError

tasks_blp = Blueprint('tasks', __name__)

@tasks_blp.route('/tasks', methods=['GET'])
def get_tasks():
    query = TaskModel.query
    check = request.args.get('completed')
    if check:
        is_completed = check.lower() == "true"
        query = query.filter_by(completed=is_completed)
    
    tasks = query.all()
    tasks_schema = TaskSchema(many=True)
    tasks_list = tasks_schema.dump(tasks)
    for task_dict in tasks_list:
        category_id = task_dict.get('category_id')
        
        if category_id:
            category = CategoryModel.query.get(category_id)
            task_dict['category'] = {
                "id": category.id,
                "name": category.name,
                "color": category.color
            }
    return jsonify(tasks_list), 200    

@tasks_blp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskModel.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task_schema = TaskSchema()
    task_dict = task_schema.dump(task)
    return jsonify(task_dict), 200

@tasks_blp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_schema = TaskSchema()
    try:
        validated = task_schema.load(data)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    
    category_id = validated.get('category_id')
    if category_id is not None:
        category = CategoryModel.query.get(category_id)
        if not category:
            return jsonify({"errors": "Category does not exist"}), 400
    
    new_task = TaskModel(**validated)
    db.session.add(new_task)
    db.session.commit()

    result_task = task_schema.dump(new_task)

    return jsonify({
        "task": result_task,
        "notification_queued": True
    }), 201

@tasks_blp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = TaskModel.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400
    task_schema = TaskSchema()
    try:
        validated = task_schema.load(data, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    if 'category_id' in validated and validated['category_id'] is not None:
        category = CategoryModel.query.get(validated['category_id'])
        if not category:
            return jsonify({"errors" : "Category not found"}), 400

    if 'title' in validated:
        task.title = validated['title']

    if 'description' in validated:
        task.description = validated['description']

    if 'completed' in validated:
        task.completed = validated['completed']

    if 'due_date' in validated:
        task.due_date = validated['due_date']

    if 'category_id' in validated:
        task.category_id = validated['category_id']
    
    db.session.commit()
    task_dict = task_schema.dump(task)
    return jsonify({'task' : task_dict}), 200

@tasks_blp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = TaskModel.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message' : 'Task deleted'})