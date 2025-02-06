import jwt
from dotenv import load_dotenv

load_dotenv()
from models.user import User
from protocols.user_repository_protocol import UserRepositoryProtocol
from datetime import datetime, timedelta, timezone


class JwtAuthenticator:
    def __init__(self, user_repository: UserRepositoryProtocol, secret: str, algorithm: str = "HS256"):
        self.user_repository = user_repository
        self.secret = secret
        self.algorithm = algorithm

    def generate_token(self, user: User, expires_in: int = 3600):
        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }

        return jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)



    def authenticate(self, token: str):
        try:
            print("test")
            print(self.secret)
            payload = jwt.decode(token, key=self.secret, algorithms=[self.algorithm])
            email = payload["email"]
            print(payload)


            if not email:
                raise Exception("Invalid Token: Email not found")

            user = self.user_repository.find_by_email(email)

            if not user:
                raise Exception("Invalid Token: User not found")
            return user

        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")

        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

