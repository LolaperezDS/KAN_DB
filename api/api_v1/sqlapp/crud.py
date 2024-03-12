from models import *



async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = (await session.execute(select(UserSQL).where(UserSQL.username == username))).scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        return False
    return user