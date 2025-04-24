import sqlite3

def create_tasks_table():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0,
            createdAt TEXT NOT NULL,
            updatedAt TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tasks_table()
