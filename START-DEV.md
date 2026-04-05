# 开发环境手动启动指南

本指南用于在**不依赖 `docker-compose`** 的情况下，手动启动项目的开发环境。仅使用 Docker 运行 MongoDB 数据库，前后端均通过本地命令启动，方便调试和学习源码。

---

## 前置依赖

请确保你的系统已安装以下工具：

- **Docker**（仅用于运行 MongoDB 容器）
- **Python 3.11+**
- **uv**（Python 包管理器，速度极快）
- **Node.js 18+** 和 **npm**

### 检查命令

```bash
docker --version
python3 --version
uv --version
node --version
npm --version
```

### 安装 uv（如未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env  # 或重新打开终端
```

---

## 步骤 1：用 Docker 启动 MongoDB

由于项目后端默认连接 `mongodb://localhost:27017`，我们只需把 MongoDB 官方容器的 `27017` 端口映射到宿主机即可。

```bash
docker run -d \
  --name blog-mongodb-dev \
  -p 27017:27017 \
  -v blog_mongo_dev_data:/data/db \
  --restart unless-stopped \
  mongo:6.0.8
```

### 验证 MongoDB 是否运行

```bash
docker ps | grep blog-mongodb-dev
```

若要进入容器内部查看数据：

```bash
docker exec -it blog-mongodb-dev mongosh
```

---

## 步骤 2：准备环境变量


### 关键变量说明

```dotenv
FASTAPI_APP_MODE=DEV               # 必须：触发加载 .env.development
FASTAPI_MONGODB_URL=mongodb://localhost:27017   # 与 Docker 映射的端口一致
FASTAPI_CREATE_TEST_USERS=True     # 启动时自动创建 Admin/Author/Reader 测试账号
VITE_API_URL="http://localhost:8000"            # 前端指向本地后端
```

> **提示**：如果 `.env.development` 里的 `FASTAPI_SECRET_KEY` 还是默认值（如 `someSecretKey`），建议替换为一个随机字符串，用于 JWT 签名：
> ```bash
> openssl rand -hex 32
> ```

---

## 步骤 3：启动后端（FastAPI）

在项目根目录下打开终端，进入 `backend` 文件夹：

```bash
cd backend

# 安装 Python 依赖（uv 会自动创建虚拟环境 .venv 并生成 uv.lock）
uv sync

# 启动开发服务器（带热重载）
uv run fastapi dev blogapp/main.py
```

启动成功后，终端会显示：

```
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

此时可以访问：
- **Swagger API 文档**：http://localhost:8000/docs
- **ReDoc 文档**：http://localhost:8000/redoc

> 因为 `FASTAPI_CREATE_TEST_USERS=True`，启动时会自动创建三个测试用户，方便你立即登录体验。

### uv 安装依赖慢？

可以指定国内 PyPI 镜像：

```bash
uv sync --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 步骤 4：启动前端（Vue3 + Vite）

**新开一个终端窗口/标签页**，进入 `frontend` 文件夹：

```bash
cd frontend

# 安装前端依赖
npm install

# 启动 Vite 开发服务器
npm run dev
```

默认会运行在 http://localhost:5173（具体以终端输出为准）。前端通过 `VITE_API_URL=http://localhost:8000` 自动连接本地后端。

---

## 验证与访问

| 服务 | 地址 | 说明 |
|------|------|------|
| Vue 前端 | http://localhost:5173 | 博客主页面 |
| FastAPI 后端 | http://localhost:8000 | API 入口 |
| Swagger 文档 | http://localhost:8000/docs | 在线调试接口 |
| MongoDB | `localhost:27017` | 由 Docker 容器提供 |

---

## 可选：重新生成前端 API Client

`frontend/src/client/` 目录下的代码是通过 OpenAPI 自动生成的。如果你后续修改了后端的 Pydantic 模型（如 `ArticleDocument`、`UserDocument` 等），需要重新生成前端类型，否则前端编译会报错。

**确保后端已启动**，然后执行：

```bash
cd frontend
npm run generate-client
```

该命令会读取 `http://localhost:8000/openapi.json` 并更新 `src/client/` 下的全部类型和请求方法。

---

## 停止服务

- **后端/前端**：在对应终端按 `Ctrl + C` 即可停止。
- **MongoDB**：
  ```bash
  docker stop blog-mongodb-dev
  ```
  如需彻底删除容器（数据仍保留在 volume `blog_mongo_dev_data` 中）：
  ```bash
  docker rm blog-mongodb-dev
  ```

---

## 常见问题

### 1. `uv sync` 下载很慢？

可以配置国内镜像源：

```bash
uv sync --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. `npm install` 很慢？

可以切换 npm 源：

```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### 3. 后端报错连接 MongoDB 失败？

- 确认 MongoDB 容器已运行：`docker ps | grep blog-mongodb-dev`
- 确认 `.env.development` 中 `FASTAPI_MONGODB_URL=mongodb://localhost:27017`
- 检查本地 `27017` 端口是否被其他进程占用

### 4. 前端报错 `Cannot find module './client/...'`？

通常是 `src/client/` 目录缺失或损坏，执行 `npm run generate-client` 重新生成即可（需后端先启动）。
