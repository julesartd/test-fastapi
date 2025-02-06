from dependency_injector import containers, providers
from authenticators.jwt_authenticator import JwtAuthenticator
from repositories.in_memory_user_repository import InMemoryUserRepository
import dotenv
import os
dotenv.load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository = providers.Singleton(InMemoryUserRepository)
    authenticator = providers.Singleton(
        JwtAuthenticator,
        user_repository=user_repository,
        secret=SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )