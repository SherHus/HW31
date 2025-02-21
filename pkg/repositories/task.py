from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from db.postgres import engine
from db.models import Task

import datetime


def get_all_tasks(user_id):
    with Session(bind=engine) as db:
        db_tasks = db.query(Task).filter(Task.deleted_at == None,
                                         Task.user_id == user_id).all()
        tasks = list()
        for task in db_tasks:
            t = Task()
            t.task_id = task.id
            t.title = task.title
            t.description = task.description
            t.deadline = task.deadline
            t.priority = task.priority
            t.is_done = task.is_done
            tasks.append(t)

        return tasks


def get_task_by_id(user_id, task_id):
    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(Task.deleted_at == None, Task.user_id == user_id,
                                        Task.id == task_id).first()
        if db_task is None:
            return None

        task = Task()
        task.task_id = db_task.id
        task.title = db_task.title
        task.description = db_task.description
        task.deadline = db_task.deadline
        task.priority = db_task.priority
        task.user_id = db_task.user_id
        task.is_done = db_task.is_done
        return task


def create_task(task: Task):
    with Session(bind=engine) as db:
        task_db = Task(title=task.title,
                       description=task.description,
                       deadline=task.deadline,
                       priority=task.priority,
                       user_id=task.user_id)
        db.add(task_db)
        db.commit()
        return task_db.id


def edit_task(task_id: int, task: Task):
    try:
        transformed_deadline = datetime.datetime.strptime(task.deadline, "%d-%m-%Y").date()
    except ValueError:
        print("Ошибка: неверный формат даты!")
        return None

    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None

        db_task.title = task.title
        db_task.description = task.description
        db_task.deadline = transformed_deadline
        db_task.priority = task.priority

        db.commit()

    return db_task


def soft_delete_task(user_id, task_id):
    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
        if not db_task:
            return None

        db_task.deleted_at = datetime.datetime.now()
        db.commit()
        return db_task


def hard_delete_task(user_id, task_id):
    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
        if not db_task:
            return None

        db.delete(db_task)
        db.commit()
        return db_task


def change_task_status(user_id: int, task_id: int, status: bool):
    with Session(bind=engine) as db:
        db_task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
        if not db_task:
            return None

        db_task.is_done = status
        db.commit()
        db.refresh(db_task)
        return db_task


def get_all_deleted_tasks(user_id):
    with Session(bind=engine) as db:
        db_tasks = db.query(Task).filter(Task.deleted_at != None,
                                         Task.user_id == user_id).all()
        tasks = list()
        for task in db_tasks:
            t = Task()
            t.task_id = task.id
            t.title = task.title
            t.description = task.description
            t.deadline = task.deadline
            t.priority = task.priority
            t.is_done = task.is_done
            tasks.append(t)

        return tasks

