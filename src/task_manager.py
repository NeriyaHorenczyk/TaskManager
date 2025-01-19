import json
import logging

from src.task import Task
from src import exceptions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TASKS_FILE = 'tasks.json'


class TaskManager:
    def __init__(self, file_name: str = TASKS_FILE):
        self.file_name: str = file_name
        self.tasks = None
        self.task_types = ["command", "reminder", "meeting"]

    def load_tasks(self, file_path):
        try:
            with open(file_path, "r") as f:
                tasks = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks]

        except FileNotFoundError as exc:
            raise exceptions.FileNotFound(f"File not found: {file_path}") from exc

    def add_task(self, description : str, due_date : str, task_type : str, command=None):
        if task_type not in self.task_types:
            raise exceptions.TaskException("Invalid task type")

        if task_type == "command" and command is None:
            raise exceptions.CommandException("Command task must have a command")

        task = Task(description, due_date, task_type, command)
        self.tasks.append(task)

    def complete_task(self, task_index):
        self.tasks[task_index].complete_a_task()

    def get_task(self, task_index):
        return self.tasks[task_index]

    def get_unfinished_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def get_finished_tasks(self):
        return [task for task in self.tasks if task.completed]

    def save_tasks(self, file_path):
        with open(self.file_name, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f,  indent=4)
