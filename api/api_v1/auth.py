from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status, APIRouter

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from sqlapp.config import SECRET_KEY, ALGHO
from service.pwd_functions import *
from pydantic_models.auth import *

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGHO
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 2  # 2 days

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")