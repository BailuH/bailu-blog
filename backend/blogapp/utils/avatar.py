from ..core.config import AVATAR_PROVIDER_URL


def is_valid_avatar_url(avatar_url: str):
    """
    检查指定的头像 URL 是否以头像提供商的 URL 开头。

    参数：
        avatar_url (str): 需要检查的头像 URL。

    返回值：
        bool: 如果头像 URL 以头像提供商的 URL 开头则返回 True，否则返回 False。
    """
    if avatar_url is None:
        return True
    if avatar_url.startswith(AVATAR_PROVIDER_URL):
        return True
    return False
