from sqlalchemy.orm import Session

import api.models.task as task_model
import api.types.task as task_type


def create_task(
    db: Session, task: task_type.TaskCreateRequest
) -> task_model.Task | None:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def read_task_by_id(db: Session, id: str) -> task_model.Task | None:
    return db.query(task_model.Task).filter(task_model.Task.id == id).first()


def update_task(
    db: Session, task: task_type.TaskUpdateRequest
) -> task_model.Task | None:
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task.id).first()
    if not db_task:
        return None
    db_task.title = task.title
    db_task.detail = task.detail
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task_by_id(db: Session, id: str) -> task_model.Task | None:
    db_task = db.query(task_model.Task).filter(task_model.Task.id == id).first()
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
