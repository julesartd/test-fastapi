from user import User


class InMemoryUserRepository:
    def __init__(self):
        self.database: list[User] = []

    
    def find_by_email(self, email: str) -> User | None:
        for user in self.database:
            if user.email == email:
                return user
        return None
    
    def create(self, user: User):
        self.database.append(user)