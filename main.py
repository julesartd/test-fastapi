from contextlib import asynccontextmanager
from fastapi import FastAPI
from container import Container
from dependency_injector.wiring import inject, Provide
from middlewares.authentication_middleware import AuthenticationMiddleware
from models.user import User
from protocols.user_repository_protocol import UserRepositoryProtocol
from routes import router
from routes.article_router import article_router
from routes.user_router import user_router

container = Container()

@asynccontextmanager
@inject
async def lifespan(api: FastAPI, user_repository: UserRepositoryProtocol = Provide[Container.user_repository]):
    user_repository.create(
        User(id="johndoe", name="John Doe", email="john.doe@mail.com", password="azerty"))
    yield

api = FastAPI(lifespan=lifespan)

container.wire(modules=[
    "routes.router",
    "middlewares.authentication_middleware",
    "routes.article_router",
    "routes.user_router",
    __name__
]) 



api.include_router(router.router)

article_api = FastAPI()
article_api.include_router(article_router)

user_api = FastAPI()
user_api.include_router(user_router)

user_api.add_middleware(AuthenticationMiddleware)
article_api.add_middleware(AuthenticationMiddleware)
api.mount("/articles", article_api)
api.mount("/users", user_api)
