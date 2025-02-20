import json

from fastapi import APIRouter, status, HTTPException

from starlette.responses import Response
from pkg.services import task as task_service

from schemas.task import TaskSchema

router = APIRouter()
"""
router: 
{
    "GET /tasks":           get_all_tasks,
    "GET /tasks/{task_id}": get_task_by_id,
    "POST /tasks":          create_task,
}
"""


@router.get("/tasks", summary="Get all tasks", tags=["tasks"])
def get_all_tasks(response: Response):
    user_id = 1
    tasks = task_service.get_all_tasks(user_id)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return tasks


@router.get("/tasks/deleted", summary="Get all deleted tasks", tags=["tasks"])
def get_all_deleted_tasks():
    user_id = 1
    tasks = task_service.get_all_deleted_tasks(user_id)
    return tasks


@router.get("/tasks/{task_id}", summary="Get task by ID", tags=["tasks"])
def get_task_by_id(task_id: int):
    user_id = 1
    task = task_service.get_task_by_id(user_id, task_id)
    if task is None:
        return Response(json.dumps({'error': 'task not found'}), status.HTTP_404_NOT_FOUND)
    return task


@router.post("/tasks", summary="Create new task", tags=["tasks"])
def create_task(task: TaskSchema):
    user_id = 1
    task_service.create_task(user_id, task)

    return Response(json.dumps({'message': 'successfully added new task'}), status_code=201,
                    media_type='application/json')


# "1. Добавить новую задачу" +
# "2. Вывести список задач" +
# "4. Вывести задачу по ID" +
# "3. Редактировать задачу" +-
# "5. Удалить задачу по ID" +-
# "6. Пометить задачу Выполнено / Не выполнено" +-
# "7. Корзина (вывод удаленных задач)"

@router.put("/tasks/{task_id}", summary="Update task by ID", tags=["tasks"])
def update_task(task_id: int, task: TaskSchema):
    user_id = 1
    task = task_service.edit_task(user_id, task_id, task)
    if task is None:
        return Response(json.dumps({'error': 'task not found'}), status.HTTP_404_NOT_FOUND)

    return Response(json.dumps({'message': 'successfully updated a task'}), status_code=status.HTTP_200_OK)


@router.delete("/tasks/{task_id}", summary="Delete task by ID", tags=["tasks"])
def delete_task(task_id: int):
    user_id = 1
    task = task_service.soft_delete_task(user_id, task_id)
    if task is None:
        return Response(json.dumps({'error': 'task not found'}), status.HTTP_404_NOT_FOUND)

    return Response(json.dumps({'message': 'successfully deleted a task'}), status_code=status.HTTP_200_OK)


# @router.delete("/tasks/{task_id}", summary="Delete task by ID", tags=["tasks"])
# def delete_task(task_id: int):
#     user_id = 1
#     task = task_service.hard_delete_task(user_id, task_id)
#     if task is None:
#         return Response(json.dumps({'error': 'task not found'}), status.HTTP_404_NOT_FOUND)
#
# return Response(json.dumps({'message': 'successfully deleted a task'}), status_code=status.HTTP_200_OK)


@router.patch("/tasks/{task_id}/status", summary="Update task status by ID", tags=["tasks"])
def update_task_status(task_id: int, is_done: bool):
    user_id = 1
    task = task_service.change_task_status(user_id, task_id, is_done)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return Response(json.dumps({'task_id': task.id, 'is_done': task.is_done}), status_code=status.HTTP_200_OK)

