
class ExtractToken:

    TOKEN_TYPES = ["bearer", "basic"]

    @staticmethod
    def extract_token(authorization: str):
        prefix, token = authorization.split(" ")
        if prefix.lower() not in ExtractToken.TOKEN_TYPES:
            raise Exception("Invalid token can't extract")
        
        return token