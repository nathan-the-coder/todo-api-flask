import sqlite3
from flask import g

DATABASE = "tasks.db"

def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    
    return g.db

def get_tasks(conn: sqlite3.Connection):
    return conn.execute("SELECT * FROM tasks").fetchall()
