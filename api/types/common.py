import strawberry


@strawberry.type
class ErrorResponse:
    message: str
