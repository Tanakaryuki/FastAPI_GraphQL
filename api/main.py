from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import strawberry
from strawberry.fastapi import GraphQLRouter

from api.schemas.user import UserMutation, UserQuery
from api.schemas.task import TaskMutation, TaskQuery
from api.db import get_db

app = FastAPI()


def get_context(request: Request, db: Session = Depends(get_db)):
    return {"db": db, "request": request}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=400,
        content={"detail": errors},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@strawberry.type
class Query(UserQuery, TaskQuery):
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Mutation(UserMutation, TaskMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)


@app.get("/")
def hello():
    return {"message": "Hello world"}


app.include_router(graphql_app, prefix="/graphql")
