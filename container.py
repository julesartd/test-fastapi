from dependency_injector import containers, providers
from authenticators.jwt_authenticator import JwtAuthenticator
from repositories.in_memory_article_repository import InMemoryArticleRepository
from repositories.in_memory_user_repository import InMemoryUserRepository
from services.encryption_service import EncryptionService
import dotenv
import os

dotenv.load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET')
FERNET_KEY = os.getenv('FERNET_KEY')
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


    encryption_service = providers.Singleton(EncryptionService, key=FERNET_KEY)

    article_repository = providers.Singleton(
        InMemoryArticleRepository,
        encryption_service=encryption_service
    )