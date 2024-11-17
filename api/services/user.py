from sqlalchemy.orm import Session

import api.cruds.user as user_crud
import api.models.user as user_model
import api.types.user as user_type
import api.utils.auth as auth


def create_user(
    db: Session, user: user_type.UserCreateRequest
) -> user_type.UserCreateResponse | ValueError:
    if user_crud.read_user_by_username(db, username=user.username):
        raise ValueError("User already exists")
    if user_crud.read_user_by_email(db, email=user.email):
        raise ValueError("Email already exists")
    hashed_password = auth.hash_password(user.password)
    new_user: user_model.User = user_model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        display_name=user.display_name,
        is_admin=user.is_admin,
    )
    return user_crud.create_user(db, user=new_user)
