from datetime import datetime

from beanie import Document, PydanticObjectId
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from ..core.security.models import UserBase
from ..core.security.roles import RolesEnum


class ExtendedDocument(Document):
    """beanie 库中 Document 的子类，包含用于扩展功能的附加方法。"""

    def check_user_can_modify_document(self, current_user: UserBase) -> None:
        """
        检查用户是否可以编辑文档。
        :raise HTTPException: 如果没有修改权限
        """
        # 允许管理员
        if current_user.role == RolesEnum.ADMIN:
            return
        # 允许编辑自己的文档
        if current_user.id == self.id:
            return
        # 允许编辑自己创作的文档
        if hasattr(self, "author"):
            if current_user.id == self.author.id:
                return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    @classmethod
    async def get_or_404(cls, document_id, fetch_links=False):
        """
        通过 Document.get() 获取并返回文档。
        如果文档未找到，则抛出状态码为 404 的 HTTPException 异常。
        """
        document = await cls.get(document_id=document_id, fetch_links=fetch_links)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )
        return document

    @classmethod
    async def update_document_by_id(
        cls,
        document_id: PydanticObjectId,
        current_user: UserBase,
        update_data: BaseModel,
    ):
        """根据 ID 更新文档。执行前会调用 check_user_can_modify_document"""

        # 获取数据
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # 检查编辑权限
        document.check_user_can_modify_document(current_user)
        # 更新数据
        document = document.model_copy(
            update=update_data.model_dump(exclude_unset=True)
        )
        document.updated_at = datetime.utcnow()
        await document.save()

        return document

    @classmethod
    async def delete_document_by_id(
        cls,
        document_id: PydanticObjectId,
        current_user: UserBase,
        link_fields_to_delete: list[str] | None = None,
    ) -> Response:
        """根据 ID 删除文档。执行前会调用 check_user_can_modify_document"""

        # 查找文档
        document = await cls.get_or_404(document_id=document_id, fetch_links=True)
        # 检查编辑权限
        document.check_user_can_modify_document(current_user)
        # 删除链接
        if link_fields_to_delete:
            for field_name in link_fields_to_delete:
                document_field_to_delete = getattr(document, field_name, None)
                if isinstance(document_field_to_delete, list):
                    for link in document_field_to_delete:
                        await link.delete()
                elif isinstance(document_field_to_delete, ExtendedDocument):
                    await document_field_to_delete.delete()
        # 删除文档
        delete_result = await document.delete()

        if delete_result:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        # 在未收到 delete_result 时的异常处理
        raise HTTPException(status_code=status.HTTP_410_GONE)
