from datetime import datetime
import sqlite3
from flask import Flask, request, jsonify
from flask import g
import db

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    conn = db.get_connection()
    if conn is not None:
        conn.close()

@app.route('/tasks', methods=["GET"])
def get_tasks():
    conn = db.get_connection()
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    task_rows = c.execute("SELECT * FROM tasks").fetchall()

    tasks = []
    for task in task_rows:
        tasks.append(dict(zip([col[0] for col in c.description], task)))

    return jsonify(tasks)

from flask import request, jsonify
from datetime import datetime

@app.route('/tasks', methods=["POST"])
def add_tasks():
    data: dict = request.get_json()
    conn = db.get_connection()

    # Ensure the data contains the required fields
    if 'title' not in data:
        return {"error": "Title is required"}, 400

    now = datetime.now().isoformat()
    title = data['title']
    description = data.get('description')  # Can be None
    completed = int(data.get('completed', 0))  # Default to 0 if not provided

    conn.execute('''
        INSERT INTO tasks (title, description, completed, createdAt)
        VALUES (?, ?, ?, ?)
    ''', (title, description, completed, now))

    conn.commit()
    return jsonify({"message": "Task added successfully!"}), 201


@app.route('/tasks/<int:task_id>', methods=["PUT"])
def update_task(task_id: int):
    data: dict = request.get_json()

    # Ensure the data contains the required fields
    if 'title' not in data or 'completed' not in data:
        return {"error": "Title and completed status are required"}, 400

    conn = db.get_connection()

    # Check if the task exists
    cursor = conn.execute('''
                 SELECT * FROM tasks WHERE id = ?
                 ''', (str(task_id)))
    task = cursor.fetchone()

    if task is None:
        return {"error": "Task not found"}, 404

    now = datetime.now().isoformat()

    # Update the task
    conn.execute('''
                 UPDATE tasks SET title = ?, description = ?, completed = ?, updatedAt = ? WHERE id = ?
                 ''', (data['title'], data.get('description'), data['completed'], now, task_id))


    conn.commit()
    conn.close()

    return {"message": "Task {data['id']} updated successfully"}, 200

@app.route('/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id: int):
    conn = db.get_connection()

    # Check if the task exists
    cursor = conn.execute('''
                 SELECT * FROM tasks WHERE id = ?
                 ''', (str(task_id)))
    task = cursor.fetchone()

    if task is None:
        return {"error": "Task not found"}, 404

    conn.execute('''
                 DELETE FROM tasks WHERE id = ?
                 ''', (str(task_id)))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
