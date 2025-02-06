from models.user import User


class AuthenticatorProtocol:

    def authenticate(self, token: str) -> User:
        raise NotImplementedError
    
    def generate_token(self, user: User) -> str:
        raise NotImplementedError