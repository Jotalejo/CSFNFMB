from fastapi import Depends, HTTPException, Request
from jose import jwt,JWTError
from config import get_settings, Settings

def get_current_user(request: Request, settings: Settings = Depends(get_settings)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=302, headers={"Location": "/login"})
