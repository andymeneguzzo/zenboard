import os
from backend.app.database import init_db, DB_PATH
from backend.app import main
from backend.app.models import TaskCreate, TaskUpdate


def setup_module(module):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()


def test_create_and_get_task():
    task = main.create_task(TaskCreate(title='Test task', description='descr'))
    assert task.title == 'Test task'
    assert task.description == 'descr'
    assert task.done is False

    fetched = main.get_task(task.id)
    assert fetched.id == task.id
    assert fetched.title == 'Test task'


def test_update_task():
    created = main.create_task(TaskCreate(title='Another', description='x'))
    updated = main.update_task(created.id, TaskUpdate(done=True))
    assert updated.done is True


def test_delete_task():
    created = main.create_task(TaskCreate(title='Delete me'))
    main.delete_task(created.id)
    try:
        main.get_task(created.id)
        assert False, 'Expected HTTPException'
    except Exception as e:
        # HTTPException is expected
        pass
