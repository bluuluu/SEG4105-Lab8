"""SQLite persistence for group tasks."""
import sqlite3
from pathlib import Path

class TaskStore:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, assignee TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)')
    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db
    def list(self):
        with self.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM tasks ORDER BY id')]
    def add(self, title, assignee):
        with self.connect() as db:
            return db.execute('INSERT INTO tasks (title, assignee) VALUES (?, ?)', (title, assignee)).lastrowid
    def complete(self, task_id):
        with self.connect() as db:
            return db.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,)).rowcount > 0
