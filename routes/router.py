from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from container import Container
from protocols.authenticator_protocol import AuthenticatorProtocol
from protocols.user_repository_protocol import UserRepositoryProtocol
from dependency_injector.wiring import Provide, inject


router = APIRouter()

@router.get("/")
async def home():
    return JSONResponse({"message": "Hello World"})

@router.post("/login")
@inject
async def login(
    credentials: dict, 
    user_repository: UserRepositoryProtocol = Depends(Provide[Container.user_repository]),
    authenticator: AuthenticatorProtocol = Depends(Provide[Container.authenticator])):
                                                               
    user = user_repository.find_by_email(credentials["email"])

    if user is None or not user.is_valid_password(credentials["password"]):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    token = authenticator.generate_token(user)
    return JSONResponse({"token": token})

