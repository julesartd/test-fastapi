from socket import inet_aton
from fastapi import HTTPException, Request
from container import Container
from protocols.authenticator_protocol import AuthenticatorProtocol
from utils.extract_token import ExtractToken
from dependency_injector.wiring import Provide, inject

@inject
def is_authenticated(request: Request, authenticator: AuthenticatorProtocol = Provide[Container.authenticator]):
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    token = ExtractToken.extract_token(authorization)

    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    try:
        user = authenticator.authenticate(token)
    except Exception as msg:
        raise HTTPException(status_code=403, detail= str(msg))
    
    request.state.user = user
    return True

