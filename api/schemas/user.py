import strawberry
from sqlalchemy.orm import Session
import strawberry.exceptions
from strawberry.types import Info

import api.services.user as user_service
import api.types.user as user_type
import api.types.common as common_type


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def createUser(
        self,
        user: user_type.UserCreateRequest,
        info: Info,
    ) -> user_type.UserCreateResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        try:
            created_user: user_type.UserCreateResponse = user_service.create_user(
                db=db,
                user=user,
            )
            return user_type.UserCreateResponse(
                uuid=created_user.uuid,
                username=created_user.username,
                email=created_user.email,
                display_name=created_user.display_name,
                is_admin=created_user.is_admin,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))

    @strawberry.mutation
    def createToken(
        self, user: user_type.UserLoginRequest, info: Info
    ) -> user_type.UserTokenResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        try:
            token = user_service.create_token(db=db, current_user=user)
            return user_type.UserTokenResponse(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                token_type=token.token_type,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))

    @strawberry.mutation
    def refreshToken(
        self, refresh_token: str, info: Info
    ) -> user_type.UserTokenResponse | common_type.ErrorResponse:
        db: Session = info.context["db"]
        try:
            token = user_service.refresh_token(db=db, refresh_token=refresh_token)
            return user_type.UserTokenResponse(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                token_type=token.token_type,
            )
        except ValueError as e:
            return common_type.ErrorResponse(message=str(e))
