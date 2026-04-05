from abc import ABC
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr

from .roles import RolesEnum


class UserBase(ABC, BaseModel):
    id: PydanticObjectId
    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None
    updated_at: datetime | None
    password_hash: str | None
    avatar_url: str | None


class TokenResponseBody(BaseModel):
    """令牌请求响应"""

    access_token: str
    token_type: str


class RegisterRequestBody(BaseModel):
    """注册请求"""

    username: str
    password: str
    email: EmailStr
