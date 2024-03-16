from models import *
from database import *
from service.pwd_functions import verify_password
from sqlalchemy import select


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = (await session.execute(select(UserTable).where(UserTable.login == username))).scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_user(username: str,
                   session: AsyncSession) -> UserTable | None:
    statement = select(UserTable).where(UserTable.username == username)
    user = (await session.execute(statement)).scalar_one_or_none()
    return user

