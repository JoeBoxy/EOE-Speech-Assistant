"""
应用配置管理 - 使用 Dynaconf
支持多环境配置、层级覆盖（settings.toml -> .secrets.toml -> 环境变量）
"""
from dynaconf import Dynaconf

# 初始化 Dynaconf
settings = Dynaconf(
    # 环境变量前缀，例如：EOE_DEBUG, EOE_DATABASE_URL
    envvar_prefix="EOE",
    
    # 配置文件列表（按优先级从低到高）
    settings_files=[
        "settings.toml",           # 通用配置
        ".secrets.toml",           # 敏感信息配置（不提交到 git）
    ],
    
    # 启用多环境支持（development / testing / production）
    environments=True,
    
    # 默认环境
    env="development",
    
    # 设置加载顺序（从低到高优先级）
    # 1. settings.toml default 部分
    # 2. settings.toml [当前环境] 部分
    # 3. .secrets.toml default 部分
    # 4. .secrets.toml [当前环境] 部分
    # 5. 环境变量（EOE_前缀）
    load_dotenv=True,
    
    # 编码
    encoding="utf-8",
)


# 配置访问方式：
#   settings.app_name
#   settings["app_name"]
#   settings.get("app_name", "default")
#   settings.get("database.url")  # 支持嵌套


def get_settings() -> Dynaconf:
    """获取配置实例"""
    return settings


# 便捷属性检查
@property
def is_development() -> bool:
    """是否为开发环境"""
    return settings.current_env.lower() == "development"


@property
def is_production() -> bool:
    """是否为生产环境"""
    return settings.current_env.lower() == "production"


@property
def is_sqlite() -> bool:
    """判断是否使用 SQLite"""
    db_url = settings.get("database_url", "")
    return db_url.startswith("sqlite")


@property
def is_mysql() -> bool:
    """判断是否使用 MySQL"""
    db_url = settings.get("database_url", "")
    return db_url.startswith("mysql")


# 将便捷属性附加到 settings 对象
settings.is_development = lambda: settings.current_env.lower() == "development"
settings.is_production = lambda: settings.current_env.lower() == "production"
settings.is_sqlite = lambda: settings.get("database_url", "").startswith("sqlite")
settings.is_mysql = lambda: settings.get("database_url", "").startswith("mysql")
