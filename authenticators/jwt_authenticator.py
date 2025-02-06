import jwt
from models.user import User
from protocols.user_repository_protocol import UserRepositoryProtocol
from protocols.authenticator_protocol import AuthenticatorProtocol
from datetime import datetime, timedelta, timezone

class JwtAuthenticator(AuthenticatorProtocol):
    def __init__(self, user_repository: UserRepositoryProtocol, secret: str, algorithm: str = "HS256"):
        self.user_repository = user_repository
        self.secret = secret
        self.algorithm = algorithm

    def generate_token(self, user: User, expires_in: int = 3600) -> str:
        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)

    def authenticate(self, token: str) -> User:
        try:
            payload = jwt.decode(token, key=self.secret, algorithms=[self.algorithm])
            email = payload["email"]
            if not email:
                raise Exception("Invalid Token: Email not found")
            user = self.user_repository.find_by_email(email)
            if not user:
                raise Exception("Invalid Token: User not found")
            return user
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError as e:
            raise Exception("Invalid token !")
    