
from fastapi import APIRouter
from fastapi.responses import JSONResponse


db = [
    {"id": "742f6277b1c741719e81bb108198f0b6","name": "John Doe","email": "john.doe@mail.com"},
    {"id": "023dff574f1f4680a3148e04a7cc9069","name": "Jane Doe","email": "jane.doe@mail.com"},
    {"id": "8f5f13a5170549cb8a674bcc81281482","name": "John Smith","email": "john.smith@mail.com"},
    {"id": "5f1d23256a274b33b8695f6287b8630e","name": "Jane Smith","email": "jane.smith@mail.com"}
]

user_router = APIRouter()

@user_router.get("/")
async def get_users():
    return JSONResponse(db)

@user_router.get("/{id}")
async def get_user(id: str):
    for user in db:
        if user["id"] == id:
            return JSONResponse(user)
    return JSONResponse({"message": "User not found"}, status_code=404)