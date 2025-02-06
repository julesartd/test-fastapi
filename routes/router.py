import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from container import Container
from models.article import Article
from protocols.authenticator_protocol import AuthenticatorProtocol
from protocols.user_repository_protocol import UserRepositoryProtocol
from middlewares.authentication_middleware import is_authenticated
from dependency_injector.wiring import Provide, inject
from repositories.in_memory_article_repository import InMemoryArticleRepository

db = [
    {"id": "742f6277b1c741719e81bb108198f0b6","name": "John Doe","email": "john.doe@mail.com"},
    {"id": "023dff574f1f4680a3148e04a7cc9069","name": "Jane Doe","email": "jane.doe@mail.com"},
    {"id": "8f5f13a5170549cb8a674bcc81281482","name": "John Smith","email": "john.smith@mail.com"},
    {"id": "5f1d23256a274b33b8695f6287b8630e","name": "Jane Smith","email": "jane.smith@mail.com"}
]

router = APIRouter()

@router.get("/")
async def home():
    return JSONResponse({"message": "Hello World"})

@router.get("/users", response_model=None)
async def get_users(is_authenticated: bool = Depends(is_authenticated)):
    if is_authenticated:
        return JSONResponse(db)

@router.get("/users/{user_id}", response_model=None)
async def get_user(user_id: str):
    for user in db:
        if user["id"] == user_id:
            return JSONResponse(user)
    return JSONResponse({"message": "User not found"}, status_code=404)

@router.post("/login", response_model=None)
@inject
async def login(
    credentials: dict, 
    user_repository: UserRepositoryProtocol = Depends(Provide[Container.user_repository]),
    authenticator: AuthenticatorProtocol = Depends(Provide[Container.authenticator])):
                                                               
    user = user_repository.find_by_email(credentials["email"])

    if user is None or not user.is_valid_password(credentials["password"]):
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    token = authenticator.generate_token(user)
    return JSONResponse({"token": token})

@router.post("/articles", response_model=None)
@inject
async def create_article(
    article_data: dict, 
    is_authenticated: bool = Depends(is_authenticated),
    article_repository: InMemoryArticleRepository = Depends(Provide[Container.article_repository])):

    if is_authenticated:
        article = Article(id=uuid.uuid4().hex, title=article_data["title"], content=article_data["content"])
        article_repository.create(article)
        return JSONResponse({"message": "Article created"})

@router.get("/articles", response_model=None)
@inject
async def get_articles(
    is_authenticated: bool = Depends(is_authenticated),
    article_repository: InMemoryArticleRepository = Depends(Provide[Container.article_repository])):

    if is_authenticated:
        articles = article_repository.get_all()
        return JSONResponse([article.dict() for article in articles])