# Liteboty Stream

Liteboty Stream 是一个基于 PySide6 的实时图像流显示程序，使用 Redis 作为消息传递机制。该程序可以订阅 Redis 频道，接收图像流，并在 GUI 窗口中展示图像。

## 特性

- 订阅 Redis 频道并实时显示图像流
- 支持动态调整窗口大小，图像自动按比例缩放
- 简单易用的 PySide6 GUI 窗口

## 安装

### 推荐安装方式（通过 `pip` 安装）

您可以通过 `pip` 安装 `liteboty-stream`，这是最简便的安装方式：

```bash
pip install liteboty-stream
```

### 从源码安装

1. 克隆此项目：

   ```bash
   git clone https://github.com/yourusername/liteboty-stream.git
   cd liteboty-stream
   ```

2. 创建一个虚拟环境并激活它：

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # 对于 Windows 用户，请使用 venv\Scripts\activate
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

4. 安装 Redis 并确保 Redis 服务正在运行。您可以按照[官方文档](https://redis.io/docs/getting-started/)安装 Redis。

## 快速开始 (Quick Start)

要启动 Liteboty Stream，使用以下命令启动应用程序：

```bash
liteboty-stream --broker <REDIS_BROKER> --decode <DECODE_FORMAT> --channel <CHANNEL>
```

### 参数说明：

- `--broker`: Redis 服务器的地址和端口（例如 `10.8.2.2:6379`）
- `--decode`: 图像解码格式（例如 `RGB` 或 `L`）
- `--channel`: Redis 频道名称（例如 `/video/raw`）

### 示例：

```bash
liteboty-stream --broker 10.8.2.128:6379 --decode RGB --channel /video/raw
```

### 运行后：

1. 应用程序将连接到指定的 Redis 服务器和频道。
2. 订阅的频道将发送图像数据，应用程序会将图像显示在窗口中。
3. 您可以调整窗口的大小，图像将按比例缩放，并且窗口的最小尺寸会自动适应图像尺寸。

## 代码结构

- `liteboty_stream.py`：主应用程序代码，包含窗口显示、图像接收和缩放逻辑。
- `redis_subscriber.py`：Redis 订阅者实现，负责从 Redis 获取图像数据。
- `requirements.txt`：项目依赖的 Python 库。

## 常见问题 (FAQ)

### 1. 如何调整窗口大小？

窗口会根据图像的大小动态调整，图像会按比例缩放以适应窗口大小。当您缩小窗口时，图像的大小也会变小。

### 2. 如何处理图像的解码？

在启动时，您可以通过 `--decode` 参数指定图像解码格式。常见的格式有 `RGB` 和 `L`（灰度图像）。
