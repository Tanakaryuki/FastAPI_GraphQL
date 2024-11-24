from sqlalchemy.orm import Session

import api.cruds.task as task_crud
import api.models.task as task_model
import api.types.task as task_type


def create_task(
    db: Session, administrator_username: str, task: task_type.TaskCreateRequest
) -> task_model.Task | ValueError:
    if task_crud.read_task_by_id(db, id=task.id):
        raise ValueError("Task already exists")
    new_task: task_model.Task = task_model.Task(
        id=task.id,
        administrator_username=administrator_username,
        title=task.title,
        detail=task.detail,
    )
    return task_crud.create_task(db, task=new_task)


def read_task(
    db: Session, administrator_username: str, id: str
) -> task_model.Task | ValueError:
    db_task = task_crud.read_task_by_id(db, id=id)
    if not db_task or db_task.administrator_username != administrator_username:
        raise ValueError("Task not found")
    return db_task


def update_task(
    db: Session, administrator_username: str, task: task_type.TaskUpdateRequest
) -> task_model.Task | ValueError:
    db_task = task_crud.read_task_by_id(db, id=task.id)
    if not db_task or db_task.administrator_username != administrator_username:
        raise ValueError("Task not found")
    update_task = task_model.Task(
        id=task.id,
        administrator_username=administrator_username,
        title=task.title,
        detail=task.detail,
    )
    return task_crud.update_task(db, task=update_task)


def delete_task(
    db: Session, administrator_username: str, id: str
) -> task_model.Task | ValueError:
    db_task = task_crud.read_task_by_id(db, id=id)
    if not db_task or db_task.administrator_username != administrator_username:
        raise ValueError("Task not found")
    return task_crud.delete_task_by_id(db, id=id)
