import sqlite3

import sqlite3
from enum import Enum

class TaskStatus(Enum):
    Todo = "Todo"
    InProgress = "In Progress"
    Completed = "Completed"

def create_tasks_table():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Get all possible values from the enum
    valid_statuses = ", ".join(f"'{status.value}'" for status in TaskStatus)
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT "{TaskStatus.Todo.value}" CHECK(status IN ({valid_statuses})),
            createdAt TEXT NOT NULL,
            updatedAt TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tasks_table()
