from datetime import datetime
import sqlite3
from flask import Flask, request, jsonify
from flask import g

app = Flask(__name__)
DATABASE = "tasks.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, ' database', None)
    if db is not None:
        db.close()

@app.route('/tasks', methods=["GET"])
def get_tasks():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    return jsonify(dict([task for task in tasks]))

@app.route('/tasks', methods=["POST"])
def add_tasks():
    data: dict = request.get_json()
    db = get_db()
    now = datetime.now().isoformat()

    db.execute('''
               INSERT INTO tasks (title, description, completed, createdAt)
               VALUES (?, ?, ?, ?)
            ''', (data['title'], data.get('description'), data['completed'], now))

    db.commit()
    return jsonify({"message": "Task added successfully!"}), 201


@app.route('/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id: int):
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            return jsonify({"message": f"Task {i} deleted successfully"}), 200

    return {"error": "Task not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
