from fastapi import HTTPException, Request

from basic_authenticator import BasicAuthenticator
from utils.extract_token import ExtractToken
from repositories.in_memory_user_repository import InMemoryUserRepository
from user import User

user_repository = InMemoryUserRepository()
user = user_repository.create(
    User(
        id="123",
        email="john.doe@mail.com",
        password="azerty",
        name="John Doe"
        )
)

authenticator = BasicAuthenticator(user_repository=user_repository)

def is_authenticated(request: Request):
    credentials = request.headers.get("Authorization")

    if not credentials:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    token = ExtractToken.extract_token(credentials)

    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    try:
        user = authenticator.authenticate(token)
    except Exception as msg:
        raise HTTPException(status_code=403, detail= str(msg))
    
    request.state.user = user
    return True

