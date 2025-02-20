from fastapi import FastAPI
from pkg.controllers.task import router as task_router
from pkg.controllers.user import router as user_router

from db.models import migrate_tables

# Создание таблиц
migrate_tables()

# Создание роутера
app = FastAPI()

# Подключаем маршруты
app.include_router(task_router)
app.include_router(user_router)

"""
[
    task_router: 
    {
        "GET /tasks":           get_all_tasks,
        "GET /tasks/{task_id}": get_task_by_id,
        "POST /tasks":          create_task,
    },
    user_router: 
    {
        "GET /users":           get_users,
    }
    
]
"""
