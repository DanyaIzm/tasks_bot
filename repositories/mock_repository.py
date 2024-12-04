from collections.abc import Iterable

from models import Task, User


class MockUserRepository:
    def __init__(self) -> None:
        self._users: list[User] = []

    def find(self, id: int) -> User | None:
        try:
            return next(filter(lambda x: x.id == id, self._users))
        except StopIteration:
            return None

    def get_users(self) -> Iterable[User]:
        return self._users

    def add_user(self, user: User) -> None:
        self._users.append(user)


class MockTaskRepository:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._current_id = 1

    def get(self, task_id: int) -> Task | None:
        try:
            return next(filter(lambda x: x.id == task_id, self._tasks))
        except StopIteration:
            return None

    def get_by_keyword(self, keyword: str) -> Iterable[Task]:
        keyword_lower = keyword.lower()

        return list(
            filter(
                lambda task: keyword_lower in task.name.lower()
                or keyword_lower in task.description.lower(),
                self._tasks,
            )
        )

    def find_completed(self) -> Iterable[Task]:
        return list(filter(lambda task: task.is_completed, self._tasks))

    def find_uncomleted(self) -> Iterable[Task]:
        return list(filter(lambda task: not task.is_completed, self._tasks))

    def get_tasks(self) -> Iterable[Task]:
        return self._tasks

    def get_tasks_by_user_id(self, user_id: int) -> Task:
        return list(filter(lambda task: task.user_id == user_id, self._tasks))

    def add_task(self, name: str, description: str, user_id: int) -> None:
        self._tasks.append(
            Task(
                id=self._current_id,
                name=name,
                description=description,
                user_id=user_id,
                is_completed=False,
            )
        )

        self._current_id += 1

    def update(self, task: Task) -> None:
        pass

    def delete_completed(self) -> None:
        self._tasks = [task for task in self._tasks if not task.is_completed]
