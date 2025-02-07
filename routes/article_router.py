import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject
from container import Container
from models.article import Article
from repositories.in_memory_article_repository import InMemoryArticleRepository

article_router = APIRouter()

@article_router.post("/", response_model=None)
@inject
async def create_article(
    article_data: dict, article_repository: InMemoryArticleRepository = Depends(Provide[Container.article_repository])):
    article = Article(id=uuid.uuid4().hex, title=article_data["title"], content=article_data["content"])

    article_repository.create(article)
    return JSONResponse({"message": "Article created"})

@article_router.get("/", response_model=None)
@inject
async def get_articles(article_repository: InMemoryArticleRepository = Depends(Provide[Container.article_repository])):
    articles = article_repository.get_all()
    return JSONResponse([article.dict() for article in articles])