class TaskException(Exception):
    pass

class TaskError(TaskException):
    pass

class FileException(Exception):
    pass

class FileNotFound(FileException):
    pass


class CommandException(Exception):
    pass
