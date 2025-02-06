from contextlib import asynccontextmanager
from fastapi import FastAPI
from container import Container
from dependency_injector.wiring import inject, Provide
from models.user import User
from protocols.user_repository_protocol import UserRepositoryProtocol
from routes import router

container = Container()

@asynccontextmanager
@inject
async def lifespan(api: FastAPI, user_repository: UserRepositoryProtocol = Provide[Container.user_repository]):
    user_repository.create(
        User(id="johndoe", name="John Doe", email="john.doe@mail.com", password="azerty"))
    yield

api = FastAPI(lifespan=lifespan)

container.wire(modules=[
    "middlewares.authentication_middleware",
    "routes.router",
    __name__
]) 

api.include_router(router.router)