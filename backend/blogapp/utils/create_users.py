# 创建具有 Admin、Author、Reader 角色的基础测试用户函数
import logging
from datetime import datetime

from ..core.security.roles import RolesEnum
from ..core.security.utilities import get_password_hash
from ..modules.users.models import UserDocument

# Add logger
log = logging.getLogger(__name__)


async def create_test_users():
    """创建基础测试用户"""

    test_users = [
        {
            "id": "65197008113d7dfdf95846f1",
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin",
            "role": RolesEnum.ADMIN.value,
        },
        {
            "id": "65197008113d7dfdf95846f2",
            "username": "author",
            "email": "author@example.com",
            "password": "author",
            "role": RolesEnum.AUTHOR.value,
        },
        {
            "id": "65197008113d7dfdf95846f3",
            "username": "reader",
            "email": "reader@example.com",
            "password": "reader",
            "role": RolesEnum.READER.value,
        },
    ]

    for user_data in test_users:
        # 检查测试用户是否已存在
        user_id_exists = await UserDocument.get(document_id=user_data["id"])
        if user_id_exists:
            # 如果密码哈希缺失，重新设置密码
            if not user_id_exists.password_hash:
                user_id_exists.password_hash = get_password_hash(user_data["password"])
                await user_id_exists.save()
                log.info(f"测试用户 {user_data['username']} 的密码已更新")
            continue

        user_name_exists = await UserDocument.find_one(
            UserDocument.username == user_data["username"]
        )
        if user_name_exists:
            log.warning(
                f"测试用户 {user_data['username']} 已存在，id 为 {user_name_exists.id}"
            )
            # 如果密码哈希缺失，重新设置密码
            if not user_name_exists.password_hash:
                user_name_exists.password_hash = get_password_hash(user_data["password"])
                await user_name_exists.save()
                log.info(f"测试用户 {user_data['username']} 的密码已更新")
            continue

        # 创建文档
        user = UserDocument(
            id=user_data["id"],
            username=user_data["username"],
            password_hash=get_password_hash(user_data["password"]),
            email=user_data["email"],
            role=user_data["role"],
            created_at=datetime.utcnow(),
        )

        # 插入文档
        await UserDocument.insert_one(user)

        log.info(f"测试用户 {user_data['username']} 已创建")
