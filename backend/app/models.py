from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool
