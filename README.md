# ZenBoard

This repository contains a minimal FastAPI backend for managing tasks. You can run the API locally and execute tests to ensure everything works as expected.

## Running the API

1. Install dependencies (already available in the Codex environment):

```bash
pip install fastapi uvicorn
```

2. Start the server:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Example Endpoints

- `GET /tasks` – list tasks
- `POST /tasks` – create a task
- `GET /tasks/{id}` – get a task
- `PUT /tasks/{id}` – update a task
- `DELETE /tasks/{id}` – delete a task

## Running Tests

This project uses `pytest` for tests:

```bash
pytest
```
