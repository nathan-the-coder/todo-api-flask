import json
from app import create_app
import db


def init_test_app(tmp_path):
    database_path = tmp_path / "test_tasks.db"
    app = create_app({"DATABASE": str(database_path)})
    with app.app_context():
        db.init_db()
    return app


def test_health_check(tmp_path):
    app = init_test_app(tmp_path)
    client = app.test_client()

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_get_task(tmp_path):
    app = init_test_app(tmp_path)
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={"title": "Read book", "description": "Read the Flask guide", "status": "Todo"},
    )
    assert response.status_code == 201

    list_response = client.get("/api/tasks")
    assert list_response.status_code == 200
    tasks = list_response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Read book"

    item_response = client.get(f"/api/tasks/{tasks[0]['id']}")
    assert item_response.status_code == 200
    task = item_response.get_json()
    assert task["status"] == "Todo"


def test_update_task(tmp_path):
    app = init_test_app(tmp_path)
    client = app.test_client()

    post_response = client.post(
        "/api/tasks",
        json={"title": "Launch app", "description": "Deploy to production", "status": "Todo"},
    )
    assert post_response.status_code == 201

    list_response = client.get("/api/tasks")
    task_id = list_response.get_json()[0]["id"]

    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Launch app", "description": "Update docs", "status": "Completed"},
    )
    assert update_response.status_code == 200

    item_response = client.get(f"/api/tasks/{task_id}")
    assert item_response.get_json()["status"] == "Completed"


def test_delete_task(tmp_path):
    app = init_test_app(tmp_path)
    client = app.test_client()

    client.post(
        "/api/tasks",
        json={"title": "Clean house", "description": "Vacuum and dust", "status": "Todo"},
    )
    tasks = client.get("/api/tasks").get_json()
    task_id = tasks[0]["id"]

    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/api/tasks/{task_id}")
    assert missing_response.status_code == 404


def test_invalid_payload(tmp_path):
    app = init_test_app(tmp_path)
    client = app.test_client()

    response = client.post("/api/tasks", json={"description": "Missing title and status"})
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()["error"]
