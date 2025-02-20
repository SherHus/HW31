from db.models import Task
from pkg.repositories import task as task_repository
from schemas.task import TaskSchema


def get_all_tasks(user_id):
    tasks = task_repository.get_all_tasks(user_id)
    return tasks


def get_task_by_id(user_id, task_id):
    task = task_repository.get_task_by_id(user_id, task_id)
    return task


def create_task(user_id: int, task: TaskSchema):
    t = Task()
    t.title = task.title
    t.description = task.description
    t.deadline = "12-12-2025"
    t.priority = task.priority
    t.is_done = False
    t.deleted_at = None
    t.user_id = user_id

    return task_repository.create_task(t)


def edit_task(user_id: int, task_id: int, task: TaskSchema):
    service_task = task_repository.get_task_by_id(user_id, task_id)
    if not service_task:
        return None

    service_task.title = task.title
    service_task.description = task.description
    service_task.deadline = task.deadline
    service_task.priority = task.priority

    return task_repository.edit_task(task_id, service_task)


def soft_delete_task(user_id, task_id):
    task = task_repository.soft_delete_task(user_id, task_id)
    return task


def hard_delete_task(user_id, task_id):
    task = task_repository.hard_delete_task(user_id, task_id)
    return task


def change_task_status(user_id: int, task_id: int, status: bool):
    task = task_repository.change_task_status(user_id, task_id, status)
    return task


def get_all_deleted_tasks(user_id):
    tasks = task_repository.get_all_deleted_tasks(user_id)
    return tasks
