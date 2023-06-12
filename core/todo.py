from dataclasses import dataclass
from colorama import Fore, Back
from tabulate import tabulate
from enum import Enum
from typing import List
import json

from core.path import Path
from core import visuals


__BLANK_CONTENT__: dict[str, dict[str, List[int]]] = {
    "todo": {
        # TASK_CONTENT: [STATE, IMPORTANCE]
    }
}


class State(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    FINISHED = 2

STATE_TRANSLATION: dict[int, str] = {
    State.PENDING.value: f"{Fore.RED}pending{Fore.RESET}",
    State.IN_PROGRESS.value: f"{Fore.YELLOW}in progress{Fore.RESET}",
    State.FINISHED.value: f"{Fore.LIGHTBLACK_EX}finished{Fore.RESET}"
}

class Importance(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

IMPORTANCE_TRANSLATION: dict[int, str] = {
    Importance.LOW.value: f"{Fore.GREEN}low{Fore.RESET}",
    Importance.MEDIUM.value: f"{Fore.YELLOW}medium{Fore.RESET}",
    Importance.HIGH.value: f"{Back.RED}high{Back.RESET}"
}



@dataclass
class Task:
    """ Represents each task. """
    content: str
    state: State
    importance: Importance

    @staticmethod
    def load_tasks_from_file(path: Path) -> List["Task"]:
        tasks = []
        with open(str(path), encoding="utf8") as file:
            content: dict[str, List[int]] = json.load(file)["todo"]

        for content, data in content.items():
            state_int, importance_int = data
            try:
                state = State(state_int)
            except ValueError:
                visuals.display_warning(f"todo: invalid state value found for: {content}")
                state = State.PENDING

            try:
                importance = Importance(importance_int)
            except ValueError:
                visuals.display_warning(f"todo: invalid importance value found for: {content}")
                importance = Importance.LOW

            task = Task(content, state, importance)
            tasks.append(task)

        return tasks


class TodoList:

    def __init__(self, path: Path) -> None:
        self.path = path
        self.tasks = Task.load_tasks_from_file(path)
        self.save()

    def display_tasks(self) -> None:
        header = ["CONTENT", "STATE", "IMPORTANCE"]
        table = []
        
        for task in self.tasks:
            state = State(task.state)
            state_name = STATE_TRANSLATION[state.value]

            content = task.content
            if state == State.FINISHED:
                content = f"{Fore.LIGHTBLACK_EX}{task.content}{Fore.RESET}"

            importance = IMPORTANCE_TRANSLATION[Importance(task.importance).value]
            table.append([content, state_name, importance])

        print(tabulate(table, headers=header, tablefmt="pretty", stralign="left", showindex=True))

    def remove_task(self, index: int) -> None:
        try:
            self.tasks.pop(index)
            self.save()
        except IndexError:
            visuals.display_error(f"todo: Invalid index: {index}")

    def append_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save()

    def as_dict(self) -> dict:
        data = {"todo": {}}
        for task in self.tasks:
            data["todo"].update({task.content: [task.state.value, task.importance.value]})
        return data

    def save(self) -> None:
        with open(str(self.path), "w+", encoding="utf8") as file:
            json.dump(self.as_dict(), file)
