class Task:
    def __init__(self, description : str, due_date : str, task_type : str, command : str = None):
        self.description = description
        self.due_date = due_date
        self.task_type = task_type
        self.command = command
        self.completed = False

    def complete_a_task(self):
        self.completed = True

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date,
            "task_type": self.task_type,
            "command": self.command,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        return cls(task_dict["description"], task_dict["due_date"], task_dict["task_type"], task_dict["command"])

    def __str__(self):
        return f"{self.task_type} - {self.description} - {self.due_date}"
