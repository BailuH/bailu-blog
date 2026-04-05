from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Body
from pydantic import EmailStr, Field, BaseModel

from ...core.config import DEFAULT_AVATAR_URL
from ...core.security.models import UserBase
from ...core.security.roles import RolesEnum
from ...utils.extended_document import ExtendedDocument


class UserDocument(ExtendedDocument, UserBase):
    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    password_hash: str | None = Field(default=None)
    avatar_url: str | None = Field(default=DEFAULT_AVATAR_URL)

    class Settings:
        name = "users"


class UpdateUserRequest(BaseModel):
    """更新用户信息的模型"""

    email: EmailStr | None = None
    avatar_url: str | None = None


class UpdateUserPasswordRequest(BaseModel):
    """更新密码的模型"""

    new_password: Annotated[str, Body(description="新密码")]
    old_password: Annotated[str | None, Body(description="旧密码")] = None


class UsersResponse(BaseModel):
    """用户列表响应模型"""

    users: list[UserDocument]


class UserResponse(BaseModel):
    """单个用户响应模型"""

    user: UserDocument


class UsersSortField(str, Enum):
    """用于排序的字段"""

    username = "username"
    created_at = "created_at"
