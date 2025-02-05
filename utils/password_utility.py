from passlib.context import CryptContext

class PasswordUtility:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash(password: str):
        return PasswordUtility._context.hash(password)

    @staticmethod
    def verify(password: str, hashed_password: str):
        return PasswordUtility._context.verify(password, hashed_password)




