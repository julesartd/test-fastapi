import base64
from protocols.user_repository_protocol import UserRepositoryProtocol


class BasicAuthenticator:

    def __init__(self, user_repository : UserRepositoryProtocol):
        self.user_repository = user_repository

    def authenticate(self, token: str):
        decoded_token = base64.b64decode(token).decode()
        email, password = decoded_token.split(":")

        user = self.user_repository.find_by_email(email)

        if user is None or password != user.password:
            raise ValueError("Invalid credentials")
        
        return user