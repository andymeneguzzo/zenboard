from fastapi import FastAPI, HTTPException
from .database import init_db, get_db
from .models import TaskCreate, TaskUpdate, Task

app = FastAPI(title="ZenBoard API")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            data = dict(row)
            data["done"] = bool(data["done"])
            result.append(Task(**data))
        return result

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (task.title, task.description),
        )
        conn.commit()
        task_id = cursor.lastrowid
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        data = dict(row)
        data["done"] = bool(data["done"])
        return Task(**data)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        data = dict(row)
        data["done"] = bool(data["done"])
        return Task(**data)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")

        data = {
            "title": task.title if task.title is not None else row["title"],
            "description": task.description if task.description is not None else row["description"],
            "done": int(task.done) if task.done is not None else row["done"],
        }
        conn.execute(
            "UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?",
            (data["title"], data["description"], data["done"], task_id),
        )
        conn.commit()
        data["done"] = bool(data["done"])
        return Task(id=task_id, **data)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return None
