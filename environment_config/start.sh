#!/bin/bash
export PATH=$PATH:/usr/bin:/usr/local/bin

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 判断有没有 "$SCRIPT_DIR/code_metrics_cron/" 文件夹，如果没有就创建
if [ ! -d "$SCRIPT_DIR/code_metrics_cron" ]; then
    mkdir "$SCRIPT_DIR/code_metrics_cron"
fi
# 获取当前时间作为日志的文件名
LOG_FILE="$SCRIPT_DIR/code_metrics_cron/$(date '+%Y-%m-%d').log"


# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# 停止cron任务的函数
stop_cron() {
    if crontab -l | grep -q "$SCRIPT_DIR"; then
        crontab -l | grep -v "$SCRIPT_DIR" | crontab -
        echo "Cron任务已停止"
        log "Cron任务已停止"
    else
        echo "未找到相关的Cron任务"
        log "未找到相关的Cron任务"
    fi
    exit 0
}

# 检查是否要停止cron任务
if [ "$1" = "stop" ]; then
    stop_cron
fi

# 设置脚本在遇到错误时立即退出
set -e

# 读取配置文件
CONFIG_FILE="$SCRIPT_DIR/sh.conf"
if [ ! -f "$CONFIG_FILE" ]; then
    log "配置文件 $CONFIG_FILE 不存在"
    exit 1
fi

# 解析配置文件
source "$CONFIG_FILE"

# 定义 Docker 镜像地址
DOCKER_IMAGE="registry.cn-hangzhou.aliyuncs.com/skt-shurima/code-metrics:$docker_image_tag"

# 检查必填项
if [ -z "$root_path" ] || [ -z "$docker_container_name" ]; then
    log "root_path 和 docker_container_name 是必填项"
    exit 1
fi

# 检查 root_path 是否存在
if [ ! -d "$root_path" ]; then
    log "root_path $root_path 不是一个有效的目录"
    exit 1
fi

# Git 操作函数
perform_git_operations() {
    log "开始 Git 操作"
    if [ -n "$git_user" ] && [ -n "$git_token" ]; then
        cd "$root_path"
        git config --global credential.helper store
        echo "https://$git_user:$git_token@github.com" > ~/.git-credentials

        # 获取默认分支
        default_branch=$(git remote show origin | grep 'HEAD branch' | cut -d' ' -f5)

        # 检查是否指定了分支
        if [ -n "$git_branch" ]; then
            log "切换到分支: $git_branch"
            if ! git checkout "$git_branch"; then
                log "切换到分支 $git_branch 失败"
                return 1
            fi
            branch_to_pull="$git_branch"
        else
            branch_to_pull="$default_branch"
        fi

        log "从远程拉取 $branch_to_pull 分支"
        if ! git pull origin "$branch_to_pull"; then
            log "Git 拉取失败"
            return 1
        fi
        cd -
        log "Git 操作完成"
    else
        log "未配置 Git 用户或 token，跳过 Git 操作"
    fi
}

# Docker 操作函数
perform_docker_operations() {
    log "开始 Docker 操作"

    # 解析 docker_volumes 配置
    IFS=',' read -ra VOLUME_MOUNTS <<< "$docker_volumes"
    VOLUME_PARAMS=""
    for i in "${VOLUME_MOUNTS[@]}"; do
        VOLUME_PARAMS="$VOLUME_PARAMS -v $i"
    done

    # 检查容器是否已存在
    if [ "$(docker ps -aq -f name=^/${docker_container_name}$)" ]; then
        if [ "$(docker ps -aq -f status=exited -f name=^/${docker_container_name}$)" ]; then
            # 容器存在但已停止，启动它
            log "启动已存在的容器"
            docker start ${docker_container_name}
        else
            log "容器已在运行中"
        fi
    else
        # 容器不存在，创建并启动它
        log "创建并启动新容器"
        docker run -d --name "$docker_container_name" \
            -m 4G \
            --cpus=2 \
            --shm-size=2g \
            $VOLUME_PARAMS \
            "$DOCKER_IMAGE" \
            tail -f /dev/null
    fi

    # 在容器中执行代码分析
    log "在容器中执行代码分析"
    docker exec ${docker_container_name} python /app/src/entry.py

    # 如果策略不是 always，则停止并删除容器
    if [ "$docker_run_strategy" != "always" ]; then
        log "停止并删除容器"
        docker stop ${docker_container_name}
        docker rm ${docker_container_name}
    fi

    log "Docker 操作完成"
}

# 主要操作函数
main_operation() {
    log "开始执行主要操作"
    perform_git_operations
    perform_docker_operations
    log "主要操作执行完成"
}

# 检查 cron 表达式
if [ -n "$cron" ]; then
    if ! crontab -l | grep -q "$SCRIPT_DIR"; then
        (crontab -l 2>/dev/null; echo "$cron cd $SCRIPT_DIR && $SCRIPT_DIR/$(basename "$0") run >> $LOG_FILE 2>&1") | crontab -
        log "已添加 cron 任务"
        echo "Cron任务已添加。要停止任务，请运行: $(readlink -f "$0") stop"
    fi
fi

if [ "$1" = "run" ]; then
    # 如果是通过 cron 或手动执行 run 命令，只执行主要操作
    main_operation
else
    # 如果没有参数，执行完整脚本
    # 拉取 Docker 镜像
    log "开始拉取 Docker 镜像"
    docker pull "$DOCKER_IMAGE"
    log "Docker 镜像拉取完成"

    main_operation
fi

log "脚本执行完成"
