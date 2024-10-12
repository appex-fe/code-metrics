import logging
import os
from logging.handlers import RotatingFileHandler

from shared.utils import get_root_path


def setup_logger(info_log_path, error_log_path, log_level=logging.INFO, max_file_size=1048576, backup_count=5):
    """
    设置日志记录器，分别处理 INFO 和 ERROR 级别的日志
    :param info_log_path: INFO 级别日志文件路径
    :param error_log_path: ERROR 级别日志文件路径
    :param log_level: 日志级别
    :param max_file_size: 单个日志文件的最大大小（字节）
    :param backup_count: 保留的日志文件数量
    :return: 配置好的日志记录器
    """
    # 创建日志目录（如果不存在）
    for path in [info_log_path, error_log_path]:
        log_dir = os.path.dirname(path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建 INFO 级别的文件处理器
    info_handler = RotatingFileHandler(
        info_log_path, maxBytes=max_file_size, backupCount=backup_count
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # 创建 ERROR 级别的文件处理器
    error_handler = RotatingFileHandler(
        error_log_path, maxBytes=max_file_size, backupCount=backup_count
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    # 可选：添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# 默认日志配置
ROOT_PATH = get_root_path()
DEFAULT_INFO_LOG_FILE = f'{ROOT_PATH}/logs/info/app_info.log'
DEFAULT_ERROR_LOG_FILE = f'{ROOT_PATH}/logs/error/app_error.log'
DEFAULT_LOG_LEVEL = logging.INFO

# 创建默认日志记录器
default_logger = setup_logger(DEFAULT_INFO_LOG_FILE, DEFAULT_ERROR_LOG_FILE, DEFAULT_LOG_LEVEL)
