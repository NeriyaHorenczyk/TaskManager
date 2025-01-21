import logging
import os
import subprocess
from datetime import datetime

from src.task import Task
from src.task_manager import TaskManager


class TaskExecutor:
    def execute_task(self, task: Task) -> None:
        if task.task_type == 'create_folder':
            os.makedirs(task.description, exist_ok=True)
        elif task.task_type == 'reminder':
            print(f"Reminder: {task.description}")
        elif task.task_type == 'run_command':
            subprocess.run(task.command, shell=True)
        task.complete_a_task()
        logging.info(f"Executed task: {task.description}")

    def check_due_tasks(self, task_manager: TaskManager) -> None:
        now = datetime.now().isoformat()
        for task in task_manager.get_unfinished_tasks():
            if task.date <= now:
                self.execute_task(task)
        task_manager.save_tasks()