from typing import Protocol

from user import User


class UserRepositoryProtocol(Protocol):
    
    def create(self, user: User) -> None:
        raise NotImplementedError

    def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError
