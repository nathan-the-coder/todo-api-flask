# Todo API Flask

A simple REST API for managing todo tasks using Flask and SQLite. This project is ready for local development and deployment with standard WSGI servers.

## Features

- CRUD operations for todo tasks
- SQLite persistence with schema initialization
- JSON validation and standardized API responses
- CORS support for frontend integration
- Ready for deployment via `gunicorn`

## Requirements

- Python 3.11+
- `pip`

## Setup

```sh
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python init_db.py
```

## Running locally

```sh
python app.py
```

The service will start on `http://127.0.0.1:5000` by default.

## Production deployment

Use a WSGI server such as `gunicorn`:

```sh
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

You can also set a custom SQLite database file path:

```sh
export DATABASE_PATH=/path/to/tasks.db
python app.py
```

### Vercel deployment

This project can be deployed to Vercel using a Python serverless function.

1. Add `vercel.json` to the repository root.
2. Add `api/index.py` with the Flask app export.
3. Ensure `requirements.txt` includes `Flask` and `Flask-Cors`.
4. Set `DATABASE_PATH` to a writable path in Vercel, for example `/tmp/tasks.db`.
5. Deploy using the Vercel CLI:

```sh
vercel --prod
```

Example Vercel environment variable configuration:

```sh
vercel env add DATABASE_PATH /tmp/tasks.db production
```

> Note: Vercel functions use ephemeral storage. A local SQLite file on Vercel is not persistent across deployments or cold starts. For production persistence, use an external database service.

Vercel will route requests to the Flask app exposed in `api/index.py`, and the app will serve API endpoints under `/api/tasks` as defined in `app.py`.

## API Endpoints

### Health check

- `GET /api/health`

Response:

```json
{
  "status": "ok"
}
```

### Get all tasks

- `GET /api/tasks`

### Get a single task

- `GET /api/tasks/<task_id>`

### Create a task

- `POST /api/tasks`

Request body:

```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "status": "Todo"
}
```

### Update a task

- `PUT /api/tasks/<task_id>`

Request body:

```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "status": "In Progress"
}
```

### Delete a task

- `DELETE /api/tasks/<task_id>`

## Example cURL commands

Create a task:

```sh
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish report", "description": "Draft the monthly report", "status": "Todo"}'
```

List tasks:

```sh
curl http://127.0.0.1:5000/api/tasks
```

Update a task:

```sh
curl -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish report", "description": "Draft and review report", "status": "Completed"}'
```

Delete a task:

```sh
curl -X DELETE http://127.0.0.1:5000/api/tasks/1
```

## Testing

Run tests with:

```sh
pytest
```

## Notes

- The API currently supports three statuses: `Todo`, `In Progress`, and `Completed`.
- SQLite is used for persistence, and `init_db.py` initializes the schema.
