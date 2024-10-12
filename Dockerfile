# 使用官方 Python 3.9 轻量级镜像作为基础镜像
FROM python:3.9-slim


RUN apt-get update && apt-get install -y wkhtmltopdf

# 设置环境变量
ENV TZ=Asia/Shanghai \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    ENVIRONMENT=production \
    PYTHONUNBUFFERED=1

# 配置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app
RUN rm -rf /app/docs /app/logs

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录并设置权限
RUN mkdir -p /app/docs /app/logs /app/.pyppeteer && \
    chmod -R 777 /app/docs /app/logs /app/.pyppeteer

# 声明卷
VOLUME ["/app/docs", "/app/logs"]

# 设置默认命令
CMD ["python", "src/entry.py"]
