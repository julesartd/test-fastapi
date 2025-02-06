from typing import Protocol
from models.user import User


class AuthenticatorProtocol(Protocol):

    def authenticate(self, token: str) -> User:
        raise NotImplementedError
    
    def generate_token(self, user: User) -> str:
        raise NotImplementedError