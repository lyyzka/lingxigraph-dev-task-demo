# lingxigraph-dev-task-demo

一个不依赖大模型的 LingxiGraph 最小技术验证项目，用于逐步演示状态图、条件路由、流式事件、人工审批、自动重试和 Checkpoint 恢复。

## 环境要求

- macOS
- Python 3.13.12
- uv
- LingxiGraph 2.x

## 安装

```bash
uv sync
```

## 启动本地开发服务器

```
uv run lingxigraph dev
```

## Studio 地址：

```
http://127.0.0.1:8124/studio/
```

## 验证 Python 版本

```
uv run python --version
```

## Develop

```bash
lingxigraph dev
```

Runs an in-memory Agent Server with an embedded Worker and opens the Studio at
http://localhost:8124/studio — no PostgreSQL or Redis required.

## Deploy (Docker Compose, single server)

```bash
lingxigraph up
```

Brings up PostgreSQL, Redis, migrations and the Agent Server (with embedded
Worker) on http://localhost:8124. Studio is served at `/studio`.

## Build the image

```bash
lingxigraph build
```

## Layout

- `lingxigraph_dev_task_demo/graph.py` — your trusted agent graph.
- `lingxigraph.json` — the manifest the Worker imports at deploy time.
- `docker-compose.yml` — single-server production topology.
