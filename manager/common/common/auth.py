from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from downloads.domain.settings import API_KEY

AUTHORIZATION = APIKeyHeader(name="authorization")


def authorizer(authorization: str = Depends(AUTHORIZATION)):
    if authorization != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return True
