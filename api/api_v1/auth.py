from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status, APIRouter

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from sqlapp.database import *

from sqlapp.config import SECRET_KEY, ALGHO
from service.pwd_functions import *
from pydantic_models.auth import *

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGHO
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 2  # 2 days

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(get_scoped_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, session=session)

    if not user:
        raise credentials_exception
    return user
