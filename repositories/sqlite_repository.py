import sqlite3
from collections.abc import Iterable

from models import Task, User


class SqliteUserRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def find(self, id: int) -> User | None:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name, phone FROM user WHERE id =?", (id,))
        row = cursor.fetchone()
        if row:
            return User(*row)

        return None

    def get_users(self) -> Iterable[User]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name, phone  FROM user")
        rows = cursor.fetchall()

        return [User(*row) for row in rows]

    def add_user(self, user: User) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO user (id, name, phone) VALUES (?, ?, ?)",
            (user.id, user.name, user.phone),
        )
        self._connection.commit()


class SqliteTaskRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get(self, task_id: int) -> Task | None:
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, user_id, name, description, is_completed FROM task WHERE id = ?",
            (task_id,),
        )
        row = cursor.fetchone()
        if row:
            return Task(*row)

        return None

    def get_by_keyword(self, keyword: str) -> Iterable[Task]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, user_id, name, description, is_completed FROM task WHERE name LIKE ? OR description LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"),
        )
        rows = cursor.fetchall()

        return [Task(*row) for row in rows]

    def find_completed(self) -> Iterable[Task]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, user_id, name, description, is_completed FROM task WHERE is_completed = 1"
        )
        rows = cursor.fetchall()

        return [Task(*row) for row in rows]

    def find_uncompleted(self) -> Iterable[Task]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, user_id, name, description, is_completed FROM task WHERE is_completed = 0"
        )
        rows = cursor.fetchall()

        return [Task(*row) for row in rows]

    def get_tasks(self) -> Iterable[Task]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, user_id, name, description, is_completed FROM task")
        rows = cursor.fetchall()

        return [Task(*row) for row in rows]

    def get_tasks_by_user_id(self, user_id: int) -> Task:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, user_id, name, description, is_completed FROM task WHERE user_id = ?",
            (user_id,),
        )
        rows = cursor.fetchall()

        return [Task(*row) for row in rows]

    def add_task(self, name: str, description: str, user_id: int) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO task (user_id, name, description, is_completed) VALUES (?, ?, ?, ?)",
            (user_id, name, description, 0),
        )
        self._connection.commit()

    def update(self, task: Task) -> None:
        cursor = self._connection.cursor()
        # VERY BAD
        cursor.execute(
            "UPDATE task SET user_id = ?, name = ?, description = ?, is_completed = ? WHERE id = ?",
            (task.user_id, task.name, task.description, task.is_completed, task.id),
        )
        self._connection.commit()

    def delete_completed(self) -> None:
        cursor = self._connection.cursor()
        # VERY BAD
        cursor.execute("DELETE FROM task WHERE is_completed = 1")
        self._connection.commit()
