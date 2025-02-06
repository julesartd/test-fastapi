from decorators.encrypt_decorator import decrypt_data, encrypt_data
from models.article import Article
from services.encryption_service import EncryptionService

class InMemoryArticleRepository:
    def __init__(self, encryption_service: EncryptionService):
        self.encryption_service = encryption_service
        self.articles: dict[str, Article] = {}

    @encrypt_data
    def create(self, article: Article):
        return article

    @decrypt_data
    def get_all(self):
        return list(self.articles.values())
    
    @decrypt_data
    def get_by_id(self, id: str) -> Article | None:
        return self.articles.get(id)