from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime(timezone=True))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now)


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7))
