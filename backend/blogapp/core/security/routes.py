from datetime import datetime, UTC
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .models import TokenResponseBody, RegisterRequestBody
from .utilities import authenticate_user, create_access_token, get_password_hash
from ...modules.users.models import UserDocument

router = APIRouter()


@router.post("/token", response_model=TokenResponseBody)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """向已认证用户发放访问令牌"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserDocument)
async def register_user(body: RegisterRequestBody):
    """创建新用户"""
    # 检查 username 和 email 是否已被占用
    existing_user = await UserDocument.find_one(UserDocument.email == body.email)

    # print(f"[DEBUG] 查询结果: {existing_user}")
    # print(f"[DEBUG] 类型: {type(existing_user)}")
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {body.email} already registered",
        )
    
    existing_user = await UserDocument.find_one(UserDocument.username == body.username)
    # print(f"[DEBUG] 查询结果: {existing_user}")
    # print(f"[DEBUG] 类型: {type(existing_user)}")
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {body.username} already registered",
        )

    user = UserDocument(
        username=body.username,
        password_hash=get_password_hash(body.password),
        email=body.email,
        disabled=False,
        created_at=datetime.now(UTC),
    )
    await UserDocument.insert_one(user)
    return user
