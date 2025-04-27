from datetime import datetime
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

import db
from contextlib import contextmanager

app = Flask(__name__)
CORS(app)

@contextmanager
def get_db_connection():
    conn = db.get_connection()
    try:
        yield conn
    finally:
        conn.close()

def getAllTasks(conn):
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            task_rows = c.execute("SELECT * FROM tasks").fetchall()
            tasks = [dict(zip([col[0] for col in c.description], task)) for task in task_rows]

            return tasks

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    try:
        with get_db_connection() as conn:
            return jsonify(getAllTasks(conn)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    try:
        with get_db_connection() as conn:
            tasks =getAllTasks(conn)
            task = [task for task in tasks if task['id'] == task_id]

            return jsonify(task), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/api/tasks", methods=["POST"])
def add_tasks():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ["title", "status"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        if data["status"] not in ["Todo", "Completed", "In Progress"]:
            return jsonify({"error": "Invalid status value"}), 400

        with get_db_connection() as conn:
            now = datetime.now().isoformat()
            conn.execute('''
                INSERT INTO tasks (title, description, status, createdAt)
                VALUES (?, ?, ?, ?)
            ''', (data["title"], data.get("description"), data["status"], now))
            conn.commit()
            
        return jsonify({"message": "Task added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=["PUT"])
def update_task(task_id: int):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ["title", "status"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()

            if task is None:
                return jsonify({"error": "Task not found"}), 404

            now = datetime.now().isoformat()
            conn.execute('''
                UPDATE tasks 
                SET title = ?, description = ?, status = ?, updatedAt = ? 
                WHERE id = ?
            ''', (data['title'], data.get('description'), data['status'], now, task_id))
            conn.commit()

        return jsonify({"message": f"Task {task_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()

            if task is None:
                return jsonify({"error": "Task not found"}), 404

            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

        return jsonify({"message": f"Task {task_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
