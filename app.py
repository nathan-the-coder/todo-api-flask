import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

import db

VALID_STATUSES = {"Todo", "In Progress", "Completed"}
DEFAULT_DATABASE = "tasks.db"


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        DATABASE=os.getenv("DATABASE_PATH", DEFAULT_DATABASE),
        JSON_SORT_KEYS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    CORS(app)
    db.init_app(app)

    def validate_task_payload(data):
        if not data or not isinstance(data, dict):
            return "No data provided"
        if "title" not in data or "status" not in data:
            return "Missing required fields: title and status"
        if not isinstance(data["title"], str) or not data["title"].strip():
            return "Title must be a non-empty string"
        if data["status"] not in VALID_STATUSES:
            return f"Invalid status value. Allowed values: {', '.join(sorted(VALID_STATUSES))}"
        return None

    def serialize_rows(rows):
        return [dict(row) for row in rows]

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        try:
            conn = db.get_db()
            rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
            return jsonify(serialize_rows(rows)), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.route("/api/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id: int):
        try:
            conn = db.get_db()
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row is None:
                return jsonify({"error": "Task not found"}), 404
            return jsonify(dict(row)), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.route("/api/tasks", methods=["POST"])
    def add_task():
        data = request.get_json()
        validation_error = validate_task_payload(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        created_at = datetime.utcnow().isoformat() + "Z"
        try:
            conn = db.get_db()
            conn.execute(
                "INSERT INTO tasks (title, description, status, createdAt) VALUES (?, ?, ?, ?)",
                (data["title"].strip(), data.get("description"), data["status"], created_at),
            )
            conn.commit()
            return jsonify({"message": "Task added successfully"}), 201
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.route("/api/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id: int):
        data = request.get_json()
        validation_error = validate_task_payload(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        updated_at = datetime.utcnow().isoformat() + "Z"
        try:
            conn = db.get_db()
            cursor = conn.execute("SELECT 1 FROM tasks WHERE id = ?", (task_id,))
            if cursor.fetchone() is None:
                return jsonify({"error": "Task not found"}), 404

            conn.execute(
                "UPDATE tasks SET title = ?, description = ?, status = ?, updatedAt = ? WHERE id = ?",
                (data["title"].strip(), data.get("description"), data["status"], updated_at, task_id),
            )
            conn.commit()
            return jsonify({"message": "Task updated successfully"}), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id: int):
        try:
            conn = db.get_db()
            cursor = conn.execute("SELECT 1 FROM tasks WHERE id = ?", (task_id,))
            if cursor.fetchone() is None:
                return jsonify({"error": "Task not found"}), 404

            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return jsonify({"message": "Task deleted successfully"}), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "0") == "1")
