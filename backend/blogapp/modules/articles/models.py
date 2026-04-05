from datetime import datetime
from enum import Enum
from typing import Annotated

import pymongo
from beanie import Link
from pydantic import BaseModel, model_validator, Field, field_validator

from ..users.models import UserDocument
from ...core.config import ARTICLE_MAX_LENGTH
from ...utils.extended_document import ExtendedDocument


class ArticleDocument(ExtendedDocument):
    title: str | None = None
    preview_image_url: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author: Link[UserDocument] | None = None

    class Settings:
        name = "articles"
        indexes = [
            [
                ("title", pymongo.TEXT),
                ("content", pymongo.TEXT),
            ]
        ]


class ArticleDocumentResponse(ArticleDocument):
    """fetch_links=True 时的响应模型"""

    author: UserDocument | None = None


class ArticleCreateOrUpdate(BaseModel):
    """创建或更新文章的模型。至少必须有一个字段不为 None"""

    title: Annotated[str, Field(min_length=2, max_length=120)] | None = None
    preview_image_url: Annotated[str, Field(max_length=120)] | None = None
    content: Annotated[str, Field(max_length=ARTICLE_MAX_LENGTH)] | None = None
    tags: Annotated[list[str], Field(max_items=20)] | None = None

    @model_validator(mode="after")
    def check_not_all_attributes_is_none(self):
        if not self.model_fields_set:
            raise ValueError("Model must have at least one not None field")
        return self

    @field_validator("preview_image_url")
    @classmethod
    def validate_preview_image_url(cls, preview_image_url: str | None) -> str | None:
        """检查该字符串是否为图片 URL"""
        if preview_image_url is None:
            return None
        is_valid_protocol = preview_image_url.startswith(("http://", "https://"))
        is_valid_extension = preview_image_url.endswith((".jpg", ".png"))

        if not (is_valid_protocol and is_valid_extension):
            raise ValueError(
                "Preview image URL must be a valid file URL with .jpg or .png extension"
            )
        return preview_image_url

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Article Title",
                    "preview_image_url": "https://example.com/image.jpg",
                    "content": "Article Text",
                    "tags": ["One", "Two"],
                }
            ]
        }
    }


class ArticleResponse(BaseModel):
    """单篇文章的响应模型"""

    article: ArticleDocumentResponse


class ArticlesResponse(BaseModel):
    """文章列表的响应模型"""

    articles: list[ArticleDocumentResponse]
    total: int


class ArticlesSortField(str, Enum):
    """用于排序的字段"""

    created_at = "created_at"
    title = "title"
