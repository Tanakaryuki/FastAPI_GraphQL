import strawberry
from datetime import datetime


@strawberry.input
class TaskCreateRequest:
    id: str
    title: str
    detail: str


@strawberry.type
class TaskDetailResponse:
    id: str
    administrator_username: str
    title: str
    detail: str
    created_at: datetime
    updated_at: datetime | None


@strawberry.input
class TaskReadRequest:
    id: str


@strawberry.input
class TaskUpdateRequest:
    id: str
    title: str
    detail: str


@strawberry.input
class TaskDeleteRequest:
    id: str
