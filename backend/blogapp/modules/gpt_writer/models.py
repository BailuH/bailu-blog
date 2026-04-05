from pydantic import BaseModel, Field

from ..articles.models import ArticleDocument


class ArticleGenerate(BaseModel):
    """生成文章的请求体"""

    title: str = Field(
        ..., min_length=2, max_length=120, examples=["ESP32 开发板的软件开发"]
    )
    tags: list[str] | None = Field(
        None, max_items=20, examples=[["编程", "ESP32"]]
    )
    key_phrases: list[str] | None = Field(
        None, max_items=20, examples=[["开发环境", "数据交换"]]
    )


class GeneratedArticleResponse(BaseModel):
    """生成文章的响应体"""

    article: ArticleDocument
    tokens_used: int
