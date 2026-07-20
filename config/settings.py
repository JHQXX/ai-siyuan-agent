"""
配置管理模块
类似 Java 中的 @ConfigurationProperties
使用 pydantic-settings 进行类型安全的配置管理
"""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载 .env 文件
# 优先从项目根目录加载
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Settings(BaseSettings):
    """应用配置类 - 所有配置都在这里集中管理"""

    # 大模型配置
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7

    # 向量数据库配置
    VECTOR_STORE_PATH: str = "./data/faiss_index"

    # 知识库配置
    KNOWLEDGE_BASE_PATH: str = "./data/knowledge_base"

    # 日志与调试
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局单例设置
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """获取全局配置单例（类似 Spring 的单例 Bean）"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def is_config_ready() -> bool:
    """检查必要配置是否已就绪（API Key 等）"""
    settings = get_settings()
    return bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_api_key_here")


def print_config_status() -> None:
    """打印配置状态，方便排查问题"""
    settings = get_settings()
    print("=" * 50)
    print("配置状态检查:")
    print(f"  LLM 模型: {settings.LLM_MODEL}")
    print(f"  API 地址: {settings.OPENAI_BASE_URL}")
    print(f"  API Key: {'已配置' if settings.OPENAI_API_KEY else '未配置!'}")
    print(f"  Temperature: {settings.LLM_TEMPERATURE}")
    print(f"  调试模式: {settings.DEBUG}")
    print("=" * 50)
