# TODO API made in Python and Flask
A simple API for a todo application, usable via cURL or programmatically.

### TODO'S
- [x] Implement a simple sqlite3 database to store persistent data.
- [ ] Polish and Refactor code for readability and documentation.
- [ ] Create a frontend cli application that uses the API.

### Features:
- Handles GET and POST requests
- Supports deleting tasks using a DELETE request.
- Uses in-memory storage (a Python list) to hold tasks during runtime.

### Endpoints

| Method | Endpoint           | Description                |
|--------|--------------------|----------------------------|
| GET    | `/tasks`           | Fetch all tasks            |
| POST   | `/tasks`           | Add a new task             |
| DELETE | `/tasks/<task_id>` | Delete a task by its ID    |


### Usage:
You can interact with this API using your app or with **cURL** from the command line.

#### Get all tasks
```sh
curl -X GET http://127.0.0.1:5000/tasks
```

#### Add a task
```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"task_title": "New Task", "task_description": "New task description"}'  http://127.0.0.1:5000/tasks 
```

#### Delete a task by ID
```sh
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

#### Running the server
Install Flask if you haven't already:
```sh
pip install Flask
```

Run the API server:
```sh
python app.py
```
This will run the server at http://127.0.0.1:5000

### LICENSE
[LICENSE](./LICENSE)
