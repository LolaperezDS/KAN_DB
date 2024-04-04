from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.users import *
from pydantic_models.kpd import *

from .auth import get_current_active_user
from .user_manager import check_acsess_level


router = APIRouter(tags=['Sanitary'])


