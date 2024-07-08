from pydantic import BaseModel, ConfigDict



class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None
