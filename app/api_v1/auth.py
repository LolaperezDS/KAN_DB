from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter

from jose import JWTError, jwt
from datetime import datetime, timedelta

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from api_v1.sqlapp.config import SECRET_KEY, ALGHO
from service.pwd_functions import *
from pydantic_models.auth import *

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGHO
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 2  # 2 days

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Annotated[AsyncSession, Depends(get_scoped_session)]) -> UserTable:
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
    user = await user
    if not user:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_active_user(
    current_user: Annotated[UserTable, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_scoped_session),
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
