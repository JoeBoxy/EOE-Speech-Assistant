"""
安全工具函数
"""
import hashlib
import secrets


def generate_random_string(length: int = 32) -> str:
    """生成随机字符串"""
    return secrets.token_urlsafe(length)[:length]


def md5_hash(text: str) -> str:
    """计算 MD5 哈希"""
    return hashlib.md5(text.encode()).hexdigest()
