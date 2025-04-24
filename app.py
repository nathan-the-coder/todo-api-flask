import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []

class Task:
    id: int
    title: str
    description: str | None
    completed: bool
    createdAt: datetime.date
    updatedAt: datetime.date | None

    def __init__(self, title: str | None, description: str | None, completed: bool):

        self.id = len(tasks) + 1
        self.title = str(title)
        self.description = description
        self.completed = completed

        self.createdAt = datetime.datetime.now().date()
        self.updatedAt = None


    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title, 
                "description": self.description, 
                "completed": self.completed,
                }
    

@app.route('/tasks', methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        return jsonify(tasks)

    elif request.method == "POST":
        data: dict = request.get_json()

        newTask = Task(data.get("task_title"), data.get("task_description"), False)

        if not newTask:
            return {"error": "Failed to get task data from the form" }, 404
        tasks.append(newTask.to_dict())

        return jsonify(newTask.to_dict()), 201

    return {}

@app.route('/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id: int):
    global tasks

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            return jsonify(deleted_task), 200
    return {"error": "Task not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
