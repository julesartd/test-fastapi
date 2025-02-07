from typing import Callable
from fastapi import HTTPException, Request, Depends
from container import Container
from protocols.authenticator_protocol import AuthenticatorProtocol
from utils.extract_token import ExtractToken
from dependency_injector.wiring import Provide, inject

from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(self, api, authenticator: AuthenticatorProtocol = Depends(Provide[Container.authenticator])):
        super().__init__(api)
        self.authenticator = authenticator

    async def dispatch(self, request: Request, call_next: Callable):
        authorization = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        token = ExtractToken.extract_token(authorization)

        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        try:
            user = self.authenticator.authenticate(token)
        except Exception as msg:
            raise HTTPException(status_code=403, detail=str(msg))
        
        request.state.user = user
        response = await call_next(request)
        return response
