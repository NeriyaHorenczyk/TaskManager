import pytest
import os

from datetime import datetime, timedelta
from src.task import Task
from src.task_manager import TaskManager
from src.task_executer import TaskExecutor
from src.exceptions import TaskError


TEST_TASK_FILE = 'test_tasks.json'

@pytest.fixture
def task_manager():
    """Fixture to create a clean TaskManager instance for each test."""
    if os.path.exists(TEST_TASK_FILE):
        os.remove(TEST_TASK_FILE)
    return TaskManager(TEST_TASK_FILE)

def test_add_task():
    task = Task("Test Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task_manager = TaskManager()
    task_manager.add_task(task)
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].description == "Test Task"

def test_mark_task_complete():
    task = Task("Complete Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task_manager = TaskManager()
    task_manager.add_task(task)
    task_manager.complete_task("Complete Task")
    assert task_manager.tasks[0].completed == True

def test_mark_task_complete_not_found():
    with pytest.raises(TaskError):
        task_manager = TaskManager()
        task_manager.complete_task("Non-existing Task")

def test_get_unfinished_tasks():
    task1 = Task("Unfinished Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task2 = Task("Completed Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task_manager = TaskManager()
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    task_manager.complete_task("Completed Task")
    unfinished_tasks = task_manager.get_unfinished_tasks()
    assert len(unfinished_tasks) == 1
    assert unfinished_tasks[0].description == "Unfinished Task"

def test_get_finished_tasks():
    task1 = Task("Unfinished Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task2 = Task("Completed Task", (datetime.now() + timedelta(days=1)).isoformat(), "reminder")
    task_manager = TaskManager()
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    task_manager.complete_task("Completed Task")
    finished_tasks = task_manager.get_finished_tasks()
    assert len(finished_tasks) == 1
    assert finished_tasks[0].description == "Completed Task"

def test_task_execution_create_folder():
    executor = TaskExecutor()
    folder_name = "test_folder"
    task = Task(folder_name, datetime.now().isoformat(), "create_folder")
    executor.execute_task(task)
    assert os.path.exists(folder_name)
    os.rmdir(folder_name)

def test_task_execution_reminder(capsys):
    executor = TaskExecutor()
    task = Task("Test Reminder", datetime.now().isoformat(), "reminder")
    executor.execute_task(task)
    captured = capsys.readouterr()
    assert "Reminder: Test Reminder" in captured.out

def test_task_execution_run_command():
    executor = TaskExecutor()
    task = Task("Echo Command", datetime.now().isoformat(), "run_command", command="echo 'Hello World'")
    executor.execute_task(task)
    assert task.completed == True

@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup after each test"""
    yield
    if os.path.exists(TEST_TASK_FILE):
        os.remove(TEST_TASK_FILE)
