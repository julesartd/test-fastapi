from functools import wraps
from models.article import Article
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from repositories.in_memory_article_repository import InMemoryArticleRepository


def encrypt_data(method: Callable):
    @wraps(method)
    def internal_wrapper(self: 'InMemoryArticleRepository', *args, **kwargs):
        data = method(self, *args, **kwargs)
        if isinstance(data, Article):
            encrypted_article = Article(
                id=self.encryption_service.encrypt(data.id),
                title=self.encryption_service.encrypt(data.title),
                content=self.encryption_service.encrypt(data.content),
            )
            self.articles[data.id] = encrypted_article
            return encrypted_article
        return data
    return internal_wrapper
    
def decrypt_data(method: Callable):
    @wraps(method)
    def internal_wrapper(self: 'InMemoryArticleRepository', *args, **kwargs):
        data = method(self, *args, **kwargs)

        if isinstance(data, Article):
            return Article(
                id=self.encryption_service.decrypt(data.id),
                title=self.encryption_service.decrypt(data.title),
                content=self.encryption_service.decrypt(data.content),
            )
        
        if isinstance(data, list):
            return [
                Article(
                    id=self.encryption_service.decrypt(article.id),
                    title=self.encryption_service.decrypt(article.title),
                    content=self.encryption_service.decrypt(article.content),
                ) for article in data
            ]
        return data
    return internal_wrapper