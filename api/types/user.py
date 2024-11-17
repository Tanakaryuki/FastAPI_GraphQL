import strawberry
from datetime import datetime
import strawberry.exceptions


@strawberry.type
class ErrorResponse:
    message: str


@strawberry.input
class UserCreateRequest:
    username: str
    email: str
    password: str
    display_name: str
    is_admin: bool


@strawberry.type
class UserCreateResponse:
    uuid: str
    username: str
    email: str
    display_name: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
