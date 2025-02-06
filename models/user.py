from pydantic import BaseModel, field_validator

from utils.password_utility import PasswordUtility

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def set_password(cls, password: str):
        return PasswordUtility.hash(password)
    
    def is_valid_password(self, password: str):
        return PasswordUtility.verify(password, self.password)