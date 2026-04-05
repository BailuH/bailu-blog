from datetime import timedelta, datetime
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from .roles import RolesEnum
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, FASTAPI_SECRET_KEY, ALGORITHM
from ...modules.users.models import UserDocument

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./token")


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    """检查密码是否与哈希匹配"""
    if not hashed_password:
        return False
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """返回密码哈希"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def get_user_by_username(username: str) -> UserDocument | None:
    """根据 username 从数据库获取用户"""
    user = await UserDocument.find_one(UserDocument.username == username)
    return user


async def authenticate_user(username: str, password: str) -> UserDocument | None:
    """根据 username 和 password 认证用户"""
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """使用字典中的数据创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, FASTAPI_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserDocument:
    """依赖项 - 根据传入的令牌返回 UserDocument"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=FASTAPI_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username)
    if not user:
        raise credentials_exception
    return user


async def get_active_current_user(
    current_user: Annotated[UserDocument, Depends(get_current_user)]
) -> UserDocument:
    """依赖项 - 返回活跃用户"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    """
    基于角色的访问控制依赖类。
    如果验证成功则返回 UserDocument
    """

    def __init__(self, allowed_role: str):
        self.allowed_role = allowed_role

    def __call__(
        self, current_user: Annotated[UserDocument, Depends(get_active_current_user)]
    ) -> UserDocument:
        allowed_role_value = RolesEnum.role_to_value(self.allowed_role)
        user_role_value = RolesEnum.role_to_value(current_user.role)
        if user_role_value < allowed_role_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        return current_user
