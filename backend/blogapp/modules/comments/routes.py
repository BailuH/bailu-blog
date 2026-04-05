from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId, Link
from beanie.odm.enums import SortDirection
from bson import DBRef
from fastapi import APIRouter, Depends, Query

from .models import (
    CommentsSortField,
    CommentsResponse,
    CommentDocument,
    CommentCreate,
    CommentResponse,
    ReplyCreate,
    CommentUpdate,
)
from ..articles.models import ArticleDocument
from ..users.models import UserDocument
from ...core.security.roles import RolesEnum
from ...core.security.utilities import RoleChecker

router = APIRouter(prefix="/comments")


@router.get("/", response_model=CommentsResponse)
async def list_comments(
    article_id: PydanticObjectId,
    skip: Annotated[int | None, Query(ge=0)] = None,  # >= 0
    limit: Annotated[int | None, Query(ge=1)] = None,  # >= 1
    sort_by: Annotated[CommentsSortField, Query()] = CommentsSortField.created_at.value,
    sort_order: Annotated[SortDirection, Query()] = SortDirection.DESCENDING.value,
):
    """返回文章评论列表"""
    # 查找文章
    _article = await ArticleDocument.get_or_404(document_id=article_id)
    # 查找评论
    comments = (
        await CommentDocument.find(
            CommentDocument.article.id == article_id,
            fetch_links=True,
        )
        .sort((sort_by, sort_order))
        .skip(n=skip)
        .limit(n=limit)
        .to_list(length=None)
    )

    return {"comments": comments}


@router.post("/", response_model=CommentResponse)
async def create_comment(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    comment_data: CommentCreate,
):
    """创建文章新评论。"""
    # 查找文章
    article = await ArticleDocument.get_or_404(document_id=comment_data.article_id)
    # 创建评论文档
    comment = CommentDocument(
        author=current_user,
        article=article,
        created_at=datetime.utcnow(),
        **comment_data.model_dump(),
    )
    # 插入评论文档
    await comment.insert()

    return {"comment": comment}


@router.post("/reply", response_model=CommentResponse)
async def create_reply(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    reply_data: ReplyCreate,
):
    """创建评论回复"""
    # 查找要回复的评论
    parent_comment = await CommentDocument.get_or_404(
        document_id=reply_data.parent_comment_id
    )
    # 创建回复文档
    reply = CommentDocument(
        author=current_user,
        is_reply=True,
        created_at=datetime.utcnow(),
        **reply_data.model_dump(),
    )
    # 插入回复文档并更新回复列表
    await reply.insert()
    parent_comment.replies.append(
        Link(
            DBRef(id=reply.id, collection=reply.get_collection_name()),
            document_class=CommentDocument,
        )
    )
    await parent_comment.save()

    return {"comment": reply}


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    comment_id: PydanticObjectId,
    comment_data: CommentUpdate,
):
    """根据 id 更新评论"""

    comment = await CommentDocument.update_document_by_id(
        document_id=comment_id,
        current_user=current_user,
        update_data=comment_data,
    )

    return {"comment": comment}


@router.delete("/{comment_id}")
async def delete_comment(
    current_user: Annotated[
        UserDocument, Depends(RoleChecker(allowed_role=RolesEnum.READER.value))
    ],
    comment_id: PydanticObjectId,
):
    """根据 id 删除评论"""
    delete_response = await CommentDocument.delete_document_by_id(
        document_id=comment_id,
        current_user=current_user,
        link_fields_to_delete=["replies"],
    )

    return delete_response
