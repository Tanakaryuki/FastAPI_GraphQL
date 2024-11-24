import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info

import api.services.task as task_service
import api.types.task as task_type
import api.types.common as common_type
import api.utils.auth as auth


@strawberry.type
class TaskMutation:
    @strawberry.mutation
    def createTask(
        self,
        task: task_type.TaskCreateRequest,
        info: Info,
    ) -> task_type.TaskDetailResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        token: str = info.context["request"].headers.get("Authorization").split(" ")[1]
        try:
            current_user = auth.get_current_user(db=db, token=token)
            created_task = task_service.create_task(
                db=db,
                administrator_username=current_user.username,
                task=task,
            )
            return task_type.TaskDetailResponse(
                id=created_task.id,
                administrator_username=created_task.administrator_username,
                title=created_task.title,
                detail=created_task.detail,
                created_at=created_task.created_at,
                updated_at=created_task.updated_at,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))

    @strawberry.mutation
    def updateTask(
        self,
        task: task_type.TaskUpdateRequest,
        info: Info,
    ) -> task_type.TaskDetailResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        token: str = info.context["request"].headers.get("Authorization").split(" ")[1]
        try:
            current_user = auth.get_current_user(db=db, token=token)
            updated_task = task_service.update_task(
                db=db,
                administrator_username=current_user.username,
                task=task,
            )
            return task_type.TaskDetailResponse(
                id=updated_task.id,
                administrator_username=updated_task.administrator_username,
                title=updated_task.title,
                detail=updated_task.detail,
                created_at=updated_task.created_at,
                updated_at=updated_task.updated_at,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))

    @strawberry.mutation
    def deleteTask(
        self,
        task: task_type.TaskDeleteRequest,
        info: Info,
    ) -> task_type.TaskDetailResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        token: str = info.context["request"].headers.get("Authorization").split(" ")[1]
        try:
            current_user = auth.get_current_user(db=db, token=token)
            deleted_task = task_service.delete_task(
                db=db,
                administrator_username=current_user.username,
                id=task.id,
            )
            return task_type.TaskDetailResponse(
                id=deleted_task.id,
                administrator_username=deleted_task.administrator_username,
                title=deleted_task.title,
                detail=deleted_task.detail,
                created_at=deleted_task.created_at,
                updated_at=deleted_task.updated_at,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))


@strawberry.type
class TaskQuery:
    @strawberry.field
    def readTask(
        self,
        id: str,
        info: Info,
    ) -> task_type.TaskDetailResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        token: str = info.context["request"].headers.get("Authorization").split(" ")[1]
        try:
            current_user = auth.get_current_user(db=db, token=token)
            task = task_service.read_task(
                db=db, administrator_username=current_user.username, id=id
            )
            return task_type.TaskDetailResponse(
                id=task.id,
                administrator_username=task.administrator_username,
                title=task.title,
                detail=task.detail,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))
