# 项目启动说明文档

本文档将指导您如何设置和运行代码度量项目。

## 1. 前置条件

- 确保已安装 Docker `apt-get install docker.io`
- 确保已安装 Git `apt-get install git`
- 确保已经安装了 cron 服务 `apt-get install cron`
- 有足够的权限执行脚本和创建 cron 任务
- 需要从`github` 拉取部分代码到指定目录
    - `cd HOST_LOCATION`
    -

## 2. 配置文件

### 2.1 sh.conf

在项目根目录下创建 `sh.conf` 文件，包含以下配置：

```
root_path=/app/project
# cron 表达式：秒 分 时 日 月 星期 年
cron="0 0 10 ? * MON *"
git_user=<Git用户名>
git_token=<Git访问令牌>
git_branch=<Git分支名>
# Docker 镜像配置，tag 一般采用 latest
docker_image_tag=<Docker镜像标签>
# 自定义容器名称 例如 code_metrics_job
docker_container_name=<Docker容器名>
# 运行策略，可选值：always、once，建议采用 always
# always：容器执行完毕后保持运行状态
# once：容器执行完毕后停止并删除
docker_run_strategy=<运行策略>
# 容器挂载配置
# docker_volumes=[HOST_LOCCATION]/config.json:/app/config.json,[HOST_LOCCATION]/docs:/app/docs/,[HOST_LOCCATION]/logs:/app/logs/,[HOST_LOCCATION]/[YOUR_PROJECT_DIR_NAME)]:/app/project/
# 这里的 [HOST_LOCCATION] 为宿主机目录，[YOUR_PROJECT_DIR_NAME] 为项目目录名
# 例如：docker_volumes=/home/code_metrics/config.json:/app/config.json,/home/code_metrics/docs:/app/docs/,/home/code_metrics/logs:/app/logs/,/home/code_metrics/project_name:/app/project/
docker_volumes=<卷挂载配置>
```

在线生成 cron 表达式：[http://www.cronmaker.com/](http://www.cronmaker.com/)
请根据实际情况修改配置参数。

### 2.2 config.json

在项目根目录下创建 `config.json` 文件，包含以下配置：

```json
{
  // 一般为 src , 这样会扫描 /app/project/src 下的文件
  "PROJECT_ROOT_DIR": "<要扫描的根目录>",
  // 代码片段匹配规则
  "code_snippets": {
    "match": [
      {
        // 匹配的文件类型，比如 java , js , py 无需带点
        "file_type": [
          "<文件类型1>",
          "<文件类型2>"
        ],
        // 匹配的代码片段，可以是纯文本，也可以是正则表达式
        "code_snippets": [
          "<代码片段1>",
          "<代码片段2>"
        ]
      }
    ],
    // 忽略的目录，相对于 PROJECT_ROOT_DIR 下的，比如 /app/project/src/test
    "ignore_dir": [
      "<忽略目录1>",
      "<忽略目录2>"
    ]
  },
  // 文件后缀匹配规则
  "find_suffix": {
    // 匹配的文件类型，比如 java , js , py 无需带点
    "file_type": [
      "<文件类型>"
    ],
    // 根据文件夹进行聚合统计，相对于 PROJECT_ROOT_DIR 下的，比如 /app/project/src/utils /app/project/src/service
    "group_by": [
      "<分组规则1>",
      "<分组规则2>"
    ],
    // 忽略的目录，相对于 PROJECT_ROOT_DIR 下的，比如 /app/project/src/test
    "ignore_dir": [
      "<忽略目录1>",
      "<忽略目录2>"
    ]
  },
  // 上述输出的信息会输出成一个 PDF 文件，这里配置文档服务器地址, 例如 http://10.10.10.10:8080
  // 注意这里的访问规则需要用户自己配置 nginx 代理
  "docs_host_port": "<文档服务器地址>",
  // 钉钉机器人配置， 每次执行完结果会发送到钉钉机器人，不配置则不会生效
  "ding_talk": {
    "token": "<钉钉机器人token>",
    "secret": "<钉钉机器人secret>"
  }
}
```

根据实际需求修改配置参数。

## 3. 启动脚本

将 `start.sh` 脚本放在项目根目录下，并赋予执行权限：

```bash
chmod +x start.sh
```

## 4. 运行项目

### 4.1 直接运行

执行以下命令直接运行项目：

```bash
./start.sh
```

这将执行以下操作：

- 拉取最新的 Docker 镜像
- 执行 Git 操作（如果配置了 Git 用户和 token）
- 创建或启动 Docker 容器
- 在容器中执行代码分析

### 4.2 设置定时任务

脚本会根据 `sh.conf` 中的 `cron` 配置自动设置 cron 任务。如果配置了有效的 cron 表达式，脚本将自动添加一个 cron 任务以定期执行。

### 4.3 停止定时任务

要停止 cron 任务，请执行：

```bash
./start.sh stop
```

## 5. 日志

脚本执行的日志将保存在 `code_metrics_cron` 目录下，以日期命名（如 `2023-05-20.log`）。

## 6. 注意事项

- 确保 `sh.conf` 中的路径配置正确，特别是 `root_path` 和 `docker_volumes`。
- 如果使用 Git 功能，请确保 `git_user` 和 `git_token` 配置正确。
- `docker_run_strategy` 设置为 `always` 时，容器将在执行完毕后保持运行状态；否则，容器将在执行后停止并删除。
- 请确保 Docker 镜像存在并可访问。

通过以上步骤，您应该能够成功设置和运行代码度量项目。如遇到问题，请查看日志文件以获取详细信息。