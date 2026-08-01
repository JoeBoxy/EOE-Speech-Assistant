# EOE演讲线上助手 Backend

EOE演讲线上助手 微信小程序后端服务 - 使用 Dynaconf 进行配置管理

## 特性

- ✅ 微信小程序登录 (code2session)
- ✅ JWT Token 认证
- ✅ 用户信息管理
- ✅ **多环境配置** (开发/测试/生产) - 使用 Dynaconf
- ✅ 支持 SQLite (本地) 和 MySQL (线上)

## 快速开始

### 1. 安装依赖

```bash
cd EOE-Speech-Assistant-backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

项目使用 **Dynaconf** 管理配置，支持多层级覆盖：

```
settings.toml (通用配置) 
    ↓
.secrets.toml (敏感信息)
    ↓
环境变量 EOE_* (最高优先级)
```

#### 步骤：

```bash
# 1. 复制敏感信息配置文件模板
cp .secrets.toml.example .secrets.toml

# 2. 编辑 .secrets.toml，填入你的配置
vim .secrets.toml
```

必需配置（在 `.secrets.toml` 中）：

```toml
[default]
wechat_appid = "wx你的小程序appid"
wechat_secret = "你的小程序secret"
secret_key = "至少32位的随机字符串"
jwt_secret_key = "另一个至少32位的随机字符串"
```

#### 可选：使用环境变量

```bash
# 设置环境
export EOE_ENV=development  # 或 production

# 覆盖任何配置
export EOE_DEBUG=true
export EOE_DATABASE_URL="mysql+aiomysql://user:pass@host:3306/dbname"
```

### 3. 启动服务

```bash
# 开发模式 (热重载，使用 SQLite)
export EOE_ENV=development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式 (使用 MySQL)
export EOE_ENV=production
export EOE_DATABASE_URL="mysql+aiomysql://user:pass@host:3306/eoe_db"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 验证运行

```bash
curl http://localhost:8000/health
# 返回: {"status":"ok","service":"EOE演讲线上助手 Backend","environment":"development"}
```

## API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs (仅开发环境)
- ReDoc: http://localhost:8000/redoc (仅开发环境)

### 接口列表

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/health` | GET | 健康检查 | 否 |
| `/api/auth/login` | POST | 微信小程序登录 | 否 |
| `/api/user/info` | GET | 获取用户信息 | 是 |
| `/api/user/info` | PUT | 更新用户信息 | 是 |

## 配置详解

### 配置文件说明

#### `settings.toml` - 通用配置

```toml
[default]           # 所有环境继承
app_name = "EOE演讲线上助手 Backend"
debug = false
jwt_expire_days = 7
database_url = "sqlite:///./data/eoe.db"

[development]       # 开发环境覆盖
debug = true
database_url = "sqlite:///./data/eoe_dev.db"

[production]        # 生产环境覆盖
debug = false
```

#### `.secrets.toml` - 敏感配置（不提交 Git）

```toml
[default]
wechat_appid = "wx..."
wechat_secret = "..."
secret_key = "..."
jwt_secret_key = "..."

[production]
# 生产环境使用不同的密钥
secret_key = "production-secret-key"
```

### 环境变量命名规则

所有配置都可以通过 `EOE_` 前缀的环境变量覆盖：

| 配置项 | 环境变量 |
|--------|----------|
| `app_name` | `EOE_APP_NAME` |
| `debug` | `EOE_DEBUG` |
| `database_url` | `EOE_DATABASE_URL` |
| `wechat_appid` | `EOE_WECHAT_APPID` |
| `jwt_secret_key` | `EOE_JWT_SECRET_KEY` |

## 数据库配置

### 本地开发 (SQLite)

默认配置，无需修改。

### 线上部署 (阿里云 MySQL)

```bash
# 方法1: 环境变量
export EOE_DATABASE_URL="mysql+aiomysql://username:password@your-rds-endpoint:3306/eoe_db"

# 方法2: .secrets.toml [production] 部分
```

MySQL 连接字符串格式：
```
mysql+aiomysql://用户名:密码@主机地址:端口/数据库名
```

## 微信小程序对接

```javascript
// pages/mine/mine.js
Page({
  async onLogin() {
    try {
      // 1. 获取微信登录 code
      const { code } = await wx.login();
      
      // 2. 获取用户信息 (可选)
      const { userInfo } = await wx.getUserProfile({
        desc: '用于完善用户资料'
      });
      
      // 3. 调用后端登录接口
      const res = await wx.request({
        url: 'https://your-api-domain.com/api/auth/login',
        method: 'POST',
        data: {
          code,
          nickname: userInfo.nickName,
          avatar_url: userInfo.avatarUrl
        }
      });
      
      if (res.data.code === 0) {
        // 保存 token
        wx.setStorageSync('token', res.data.data.token);
        wx.showToast({ title: '登录成功' });
      }
    } catch (err) {
      console.error('登录失败:', err);
    }
  }
})
```

## 项目结构

```
EOE-Speech-Assistant-backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # Dynaconf 配置
│   ├── models/              # 数据库模型
│   ├── routers/             # API 路由
│   ├── services/            # 业务逻辑
│   ├── schemas/             # 数据验证
│   ├── middlewares/         # 中间件
│   └── utils/               # 工具函数
├── data/                    # SQLite 数据目录
├── settings.toml            # 通用配置
├── .secrets.toml            # 敏感配置 (gitignore)
├── .secrets.toml.example    # 敏感配置模板
├── requirements.txt
└── README.md
```

## 部署

### 生产环境配置

1. 创建 `.secrets.toml` 并设置强密钥
2. 设置环境变量 `EOE_ENV=production`
3. 配置阿里云 MySQL 连接
4. 配置 HTTPS (微信小程序要求)

### 使用 systemd

```ini
# /etc/systemd/system/eoe.service
[Unit]
Description=EOE演讲线上助手 Backend
After=network.target

[Service]
Type=simple
User=www
WorkingDirectory=/path/to/EOE-Speech-Assistant-backend
Environment=EOE_ENV=production
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 使用 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV EOE_ENV=production

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 开发规范

- 使用 Python 3.11+ 语法
- 添加类型注解
- 异步函数使用 `async/await`
- API 响应统一格式: `{code, message, data}`

## 参考

- [Dynaconf 文档](https://www.dynaconf.com/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [微信小程序登录文档](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/login.html)

## License

MIT
