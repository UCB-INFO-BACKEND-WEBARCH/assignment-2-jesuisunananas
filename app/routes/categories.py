from flask import Blueprint, jsonify, request
from app.models import db, TaskModel, CategoryModel
from app.schemas import CategorySchema, TaskSchema
from marshmallow import ValidationError

categories_blp = Blueprint('categories', __name__)

@categories_blp.route('/categories', methods=['GET'])
def get_categories():
    categories = CategoryModel.query.all()
    category_schema = CategorySchema()
    categories_list = []

    for category in categories:
        check = category_schema.dump(category)
        count = TaskModel.query.filter_by(category_id = category.id).count()
        check['task_count'] = count
        categories_list.append(check)

    return jsonify({"categories": categories_list}), 200

@categories_blp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = CategoryModel.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    category_schema = CategorySchema()
    task_schema = TaskSchema(only=("id", "title", "completed"))
    tasks = TaskModel.query.filter_by(category_id=category.id).all()
    all_tasks = []
    category_dict = category_schema.dump(category)

    for task in tasks:
        check = task_schema.dump(task)
        all_tasks.append(check)

    category_dict['tasks'] = all_tasks

    return jsonify(category_dict), 200

@categories_blp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category_schema = CategorySchema()
    try:
        validated = category_schema.load(data)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    
    if CategoryModel.query.filter_by(name=validated['name']).first():
        return jsonify({"errors": {"name": ["Category with this name already exists."]}}), 400

    new_category = CategoryModel(**validated)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "created"}), 201
    

@categories_blp.route('/categories/<int:category_id>', methods=["DELETE"])
def delete_category(category_id):
    category = CategoryModel.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    count = TaskModel.query.filter_by(category_id = category.id).count()
    if count > 0:
        return jsonify({"error": "Cannot delete category with existing tasks. Move or delete tasks first."}), 400
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message' : 'Category deleted'})
    