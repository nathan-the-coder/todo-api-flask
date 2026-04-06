import sqlite3
from flask import current_app, g

DEFAULT_STATUSES = ["Todo", "In Progress", "Completed"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db_conn = g.pop("db", None)
    if db_conn is not None:
        db_conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def create_tasks_table(conn):
    valid_statuses = ", ".join(f"'{status}'" for status in DEFAULT_STATUSES)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Todo' CHECK(status IN ({valid_statuses})),
            createdAt TEXT NOT NULL,
            updatedAt TEXT
        )
    """)
    conn.commit()


def init_db():
    conn = get_db()
    create_tasks_table(conn)
