from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from container import Container
from middlewares.authentication_middleware import is_authenticated
from dependency_injector.wiring import inject, Provide

from models.user import User
from protocols.authenticator_protocol import AuthenticatorProtocol
from protocols.user_repository_protocol import UserRepositoryProtocol

db = [
    {"id": "742f6277b1c741719e81bb108198f0b6","name": "John Doe","email": "john.doe@mail.com"},
    {"id": "023dff574f1f4680a3148e04a7cc9069","name": "Jane Doe","email": "jane.doe@mail.com"},
    {"id": "8f5f13a5170549cb8a674bcc81281482","name": "John Smith","email": "john.smith@mail.com"},
    {"id": "5f1d23256a274b33b8695f6287b8630e","name": "Jane Smith","email": "jane.smith@mail.com"}
]

api = FastAPI()

@api.get("/")
async def home():
    return JSONResponse({"message": "Hello World"})


@api.get("/users")
async def get_users(is_authenticated: bool = Depends(is_authenticated)):
    if is_authenticated:
        return JSONResponse(db)

@api.get("/users/{user_id}")
async def get_user(user_id: str):
    for user in db:
        if user["id"] == user_id:
            return JSONResponse(user)
    return JSONResponse({"message": "User not found"}, status_code=404)

@api.post("/login")
async def login(credentials: dict,
                user_repository: UserRepositoryProtocol = Depends(Provide[Container.user_repository]),
                authenticator: AuthenticatorProtocol = Depends(Provide[Container.authenticator])
                ):
                                                               

    user = user_repository.find_by_email(credentials["email"])

    if user is None or not user.is_valid_password(credentials["password"]):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    token = authenticator.generate_token(user)
    return JSONResponse({"token": token})


if __name__ == "__main__":
    container = Container()

    container.wire(modules=[
        "middlewares.authentication_middleware",
    __name__,

    ])

    @inject
    def create_user(user_repository: UserRepositoryProtocol = Provide[Container.user_repository]):
        user_repository.create(
            User(
                id="johndoe",
                name="John Doe",
                email="john.doe@mail.com",
                password="azerty"
            )
        )
    create_user()
    