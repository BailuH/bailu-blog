from typing import Annotated

from beanie import PydanticObjectId
from beanie.odm.enums import SortDirection
from fastapi import APIRouter, Depends, Query, Path, HTTPException, Body
from starlette import status

from ...utils.avatar import is_valid_avatar_url
from .models import (
    UserDocument,
    UsersResponse,
    UsersSortField,
    UserResponse,
    UpdateUserRequest,
    UpdateUserPasswordRequest,
)
from ...core.security.roles import RolesEnum
from ...core.security.utilities import (
    RoleChecker,
    get_active_current_user,
    verify_password,
    get_password_hash,
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=UsersResponse)
async def list_users(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    skip: Annotated[int | None, Query(ge=0)] = None,  # >= 0
    limit: Annotated[int | None, Query(ge=1)] = None,  # >= 1
    sort_by: Annotated[UsersSortField, Query()] = UsersSortField.created_at.value,
    sort_order: Annotated[SortDirection, Query()] = SortDirection.DESCENDING.value,
):
    """返回用户列表"""

    # 基础查询
    query = UserDocument.find(fetch_links=True)
    # 排序、分页
    query = query.sort((sort_by, sort_order)).skip(n=skip).limit(n=limit)
    # 获取用户列表
    users = await query.to_list(length=None)

    return {"users": users}


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[UserDocument, Depends(get_active_current_user)],
):
    """返回当前用户"""

    return {"user": current_user}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="用户 UUID")],
):
    """根据 id 返回用户"""

    user = await UserDocument.get_or_404(document_id=user_id)

    return {"user": user}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="用户 UUID")],
    user_data: UpdateUserRequest,
):
    """根据 id 更新用户数据"""

    if not is_valid_avatar_url(user_data.avatar_url):
        raise HTTPException(status_code=400, detail="头像 URL 格式无效")

    updated_user = await UserDocument.update_document_by_id(
        document_id=user_id,
        current_user=current_user,
        update_data=user_data,
    )

    return {"user": updated_user}


@router.put("/{user_id}/password")
async def update_user_password(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    user_id: Annotated[PydanticObjectId, Path(description="用户 UUID")],
    password_data: UpdateUserPasswordRequest,
):
    """根据 id 更新用户密码"""

    user = await UserDocument.get_or_404(document_id=user_id)
    user.check_user_can_modify_document(current_user)
    # 如果更新的是当前用户的个人资料，进行校验
    if user.id == current_user.id:
        # 核对旧密码
        if not verify_password(
            plain_password=password_data.old_password,
            hashed_password=current_user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="密码错误",
            )
    # 如果不是更新自己的账户
    else:
        # 禁止更改其他管理员的密码
        if user.role == RolesEnum.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无法更改其他管理员的密码",
            )
    # 写入新密码
    user.password_hash = get_password_hash(password_data.new_password)
    await user.save()

    return {"message": "密码已更新"}


@router.put("/{user_id}/disable")
async def disable_user(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.ADMIN.value))
    ],
    user_id: str = Path(description="用户 UUID"),
):
    """根据 id 禁用用户 [管理员]"""

    user = await UserDocument.get_or_404(document_id=user_id)
    # 禁止禁用管理员
    if user.role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法禁用管理员",
        )
    # 禁用用户
    user.disabled = True
    await user.save()

    return {"message": "用户已成功禁用"}


@router.put("/{user_id}/role")
async def change_user_role(
    _current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.ADMIN.value))
    ],
    user_id: Annotated[str, Path(description="用户 UUID")],
    role: Annotated[RolesEnum, Body(embed=True, description="角色")],
):
    """根据 id 更改用户角色 [管理员]"""

    user = await UserDocument.get_or_404(document_id=user_id)
    # 禁止分配管理员角色
    if role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法分配管理员角色",
        )
    # 禁止更改管理员角色
    if user.role == RolesEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法更改管理员角色",
        )
    # 更改角色
    user.role = role
    await user.save()

    return {"message": f"用户已被分配角色 {role.value}"}
