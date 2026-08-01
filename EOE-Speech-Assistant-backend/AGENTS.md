# EOE演讲线上助手 Backend

## 项目简介

EOE演讲线上助手 微信小程序后端服务，提供用户登录和基础用户信息管理功能。

## 技术栈

- **框架**: FastAPI + Uvicorn
- **数据库**: SQLAlchemy 2.0 (支持 SQLite 本地 / MySQL 线上)
- **认证**: JWT (PyJWT)
- **配置**: **Dynaconf** (多环境配置管理)

## 配置管理 (Dynaconf)

### 配置文件层级 (优先级从低到高)

1. `settings.toml` - 通用配置 (可提交到 Git)
2. `.secrets.toml` - 敏感信息配置 (不提交到 Git)
3. 环境变量 (`EOE_*` 前缀) - 最高优先级

### 多环境支持

```
[default]      # 所有环境继承
[development]  # 开发环境 (默认)
[testing]      # 测试环境
[production]   # 生产环境
```

切换环境:
```bash
# 方式1: 环境变量
export EOE_ENV=production

# 方式2: 配置文件 settings.toml
[production]
...
```

### 配置访问方式

```python
from app.config import settings

# 属性访问
settings.app_name
settings.database_url

# 字典访问
settings["app_name"]
settings.get("app_name", "default")

# 便捷方法
settings.is_development()  # 是否开发环境
settings.is_production()   # 是否生产环境
settings.is_sqlite()       # 是否使用 SQLite
settings.is_mysql()        # 是否使用 MySQL
```

### 环境变量覆盖

任何配置都可以通过环境变量覆盖，命名规则：`EOE_` + 大写配置名

```bash
# settings.toml 中的 app_name -> EOE_APP_NAME
# settings.toml 中的 database_url -> EOE_DATABASE_URL

export EOE_DEBUG=true
export EOE_DATABASE_URL="mysql+aiomysql://user:pass@host/db"
export EOE_JWT_SECRET_KEY="your-secret-key"
```

## 项目结构

```
app/
├── main.py              # FastAPI 应用入口
├── config.py            # Dynaconf 配置实例
├── models/
│   ├── base.py          # SQLAlchemy Base + 引擎 + 会话
│   └── user.py          # 用户模型
├── routers/
│   ├── auth.py          # POST /api/auth/login
│   └── user.py          # GET/PUT /api/user/info
├── services/
│   ├── wechat.py        # 微信 API 封装
│   └── auth.py          # JWT Token 生成/验证
├── schemas/
│   ├── base.py          # 统一响应格式
│   ├── auth.py          # 登录请求/响应模型
│   └── user.py          # 用户信息模型
└── middlewares/
    └── auth.py          # JWT 验证中间件
```

## 核心流程

### 微信登录流程

1. 小程序 `wx.login()` 获取 `code`
2. 发送到 `POST /api/auth/login` (携带 code)
3. 后端调用微信 `code2session` 换取 `openid`
4. 查询或创建用户 (openid 唯一)
5. 生成 JWT token 返回
6. 小程序存储 token，后续请求携带在 Header: `Authorization: Bearer <token>`

## 关键配置项

### 必需配置

```toml
# .secrets.toml
[default]
wechat_appid = "wx1234567890abcdef"
wechat_secret = "your-wechat-secret"
secret_key = "your-app-secret-key-min-32-chars"
jwt_secret_key = "your-jwt-secret-key-min-32-chars"
```

### 数据库配置

```toml
# settings.toml
[default]
database_url = "sqlite:///./data/eoe.db"  # 本地开发

[production]
database_url = "mysql+aiomysql://user:pass@host:3306/dbname"  # 线上 MySQL
```

## API 规范

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 微信登录失败 |
| 1002 | Token 无效或过期 |
| 500 | 服务器内部错误 |

## 开发指南

### 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 复制配置文件
cp .secrets.toml.example .secrets.toml
# 编辑 .secrets.toml 填入你的配置

# 3. 启动开发服务器
uvicorn app.main:app --reload
```

### 多环境开发

```bash
# 开发环境 (默认)
export EOE_ENV=development
uvicorn app.main:app --reload

# 生产环境测试
export EOE_ENV=production
export EOE_DATABASE_URL="mysql+aiomysql://..."
uvicorn app.main:app
```

## 部署注意事项

1. 创建 `.secrets.toml` 并设置强密钥
2. 设置 `EOE_ENV=production`
3. 配置 MySQL 连接字符串
4. 配置 HTTPS (微信小程序要求)
5. 在小程序后台配置 request 合法域名
