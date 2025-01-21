import argparse

from src.task import Task
from src.task_executer import TaskExecutor
from src.task_manager import TaskManager


class CLIHandler:
    def __init__(self) -> None:
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor()

    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Task Management System')
        parser.add_argument('--add', nargs=3, metavar=('desc', 'date', 'type'), help='Add a new task')
        parser.add_argument('--cmd', metavar='command', help='Command to run for run_command type')
        parser.add_argument('--complete', metavar='desc', help='Mark task as complete')
        parser.add_argument('--list', choices=['pending', 'completed'], help='List tasks')
        return parser.parse_args()

    def run(self) -> None:
        args = self.parse_arguments()
        self.task_executor.check_due_tasks(self.task_manager)

        if args.add:
            task = Task(args.add[0], args.add[1], args.add[2], args.cmd)
            self.task_manager.add_task(task)
        elif args.complete:
            self.task_manager.complete_task(args.complete)
        elif args.list:
            tasks = self.task_manager.get_finished_tasks() if args.list == 'completed' else self.task_manager.get_unfinished_tasks()
            for task in tasks:
                print(task.to_dict())