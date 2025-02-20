from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    description: str
    priority: str
    deadline: str




