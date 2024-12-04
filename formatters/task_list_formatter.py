from collections.abc import Iterable
from typing import Any

from aiogram.utils import formatting

from models import Task


def get_formatted_task_list(tasks: Iterable[Task]) -> dict[str, Any]:
    return formatting.as_list(
        *[
            formatting.as_section(
                formatting.Bold(
                    f"{task.name} {'✅' if task.is_completed else '❌'}",
                ),
                formatting.Bold(f"id: {task.id}\n"),
                task.description,
            )
            for task in tasks
        ],
        sep="\n\n",
    ).as_kwargs()
