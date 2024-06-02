from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db/tasks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, completed):
        self.title = title
        self.description = description
        self.completed = completed

# Task schema
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

# Initialize schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create a Task
@app.route('/task', methods=['POST'])
def add_task():
    title = request.json['title']
    description = request.json['description']
    completed = request.json['completed']
    
    new_task = Task(title, description, completed)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

# Get All Tasks
@app.route('/task', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Get Single Task
@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# Update a Task
@app.route('/task/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    title = request.json['title']
    description = request.json['description']
    completed = request.json['completed']

    task.title = title
    task.description = description
    task.completed = completed

    db.session.commit()

    return task_schema.jsonify(task)

# Delete Task
@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
print("FLASK_APP:", os.getenv('FLASK_APP'))
print("FLASK_RUN_HOST:", os.getenv('FLASK_RUN_HOST'))
