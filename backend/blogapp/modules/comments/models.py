from datetime import datetime
from enum import Enum

from beanie import Link, PydanticObjectId
from pydantic import BaseModel, Field

from ..articles.models import ArticleDocument
from ..users.models import UserDocument
from ...utils.extended_document import ExtendedDocument


class CommentDocument(ExtendedDocument):
    content: str
    author: Link[UserDocument]
    disabled: bool = False
    is_reply: bool = False
    article: Link[ArticleDocument] | None = Field(None, exclude=True)
    replies: list[Link["CommentDocument"]] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "comments"


class CommentDocumentResponse(CommentDocument):
    """fetch_links=True 时的响应模型"""
    author: UserDocument
    replies: list[CommentDocument]


class CommentUpdate(BaseModel):
    """修改评论的请求体"""

    content: str = Field(..., min_length=2, max_length=120)


class CommentCreate(CommentUpdate):
    """创建评论的请求体"""

    article_id: PydanticObjectId = Field(..., exclude=True)


class ReplyCreate(CommentUpdate):
    """创建评论回复的请求体"""

    parent_comment_id: PydanticObjectId = Field(..., exclude=True)


class CommentsResponse(BaseModel):
    comments: list[CommentDocumentResponse]


class CommentResponse(BaseModel):
    comment: CommentDocumentResponse


class CommentsSortField(str, Enum):
    created_at = "created_at"
