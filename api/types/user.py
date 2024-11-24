import strawberry
from datetime import datetime


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


@strawberry.input
class UserLoginRequest:
    username: str
    password: str


@strawberry.type
class UserTokenResponse:
    access_token: str
    refresh_token: str
    token_type: str


@strawberry.input
class UserRefreshTokenRequest:
    refresh_token: str


@strawberry.type
class UserInformationResponse:
    uuid: str
    username: str
    email: str
    display_name: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None
