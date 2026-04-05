import logging
from pathlib import Path

import langdetect
import openai
from fastapi import HTTPException
import yaml

from ...core.config import BACKEND_DIR_PATH

log = logging.getLogger("blogapp")


class Writer:
    """与 ChatGPT 交互的类"""

    settings: dict

    @classmethod
    def init_writer(cls, host: str, api_key: str):
        """
        初始化 Writer。准备 openai 库并从 .yml 获取设置
        :param host: API 服务器。如果为空，则使用标准 OpenAI 端点。
        :param api_key: API 密钥。
        """

        # 在 openai 中配置 Host 和 API 密钥
        if not (host == "" or host == "https://api.openai.com/v1"):
            openai.api_base = host
        openai.api_key = api_key

        # 加载提示词设置
        settings_path = Path(
            BACKEND_DIR_PATH, "blogapp", "modules", "gpt_writer", "chatgpt_settings.yml"
        )
        with open(settings_path, "r", encoding="utf-8") as file:
            cls.settings = yaml.safe_load(file)

    @classmethod
    def prepare_article_generation_prompt(
        cls, title: str, tags: list | None, key_phrases: list | None
    ) -> str:
        prompt = cls.settings["prompt"].format(
            title=title,
            tags=(tags if tags else "[ai generated]"),
            key_phrases=(key_phrases if key_phrases else "[Ai generated text]"),
        )
        # 函数名用于日志
        log.debug(f"在 prepare_article_generation_prompt 函数中创建了提示词 {prompt}")
        return prompt

    @classmethod
    async def generate_article_content(cls, prompt: str = ""):
        """
        通过 ChatGPT 生成文章文本
        :param prompt: 用于生成的提示词
        :return: OpenAIObject - chat completion object
        :raises HTTPException: 在任何可能的错误时
        """

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            log.error(str(e))
            raise HTTPException(status_code=500, detail=str(e))

        return response

    @classmethod
    def check_article(cls, article_text) -> list:
        """检查文章文本是否存在错误并返回发现的错误列表。"""
        error_list = []

        # 是否包含超过 50 个词
        if len(article_text.split()) < 50:
            error_list.append("文章必须包含超过 50 个词")

        # 是否用中文撰写
        if langdetect.detect(article_text) != "zh-cn":
            error_list.append("文章必须用中文撰写")

        return error_list
