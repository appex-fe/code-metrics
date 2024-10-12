# 入口文件，如果对应的配置信息不为空，则启动对应的服务
import sys
import os
from config import FIND_CODE_SNIPPET, FIND_SUFFIX, PROJECT_ROOT
from find_code_snippet.main import main as find_code_snippet_main
from find_suffix.main import main as find_suffix_main
from shared.logger import default_logger as logger

if __name__ == '__main__':
    if not os.path.isdir(PROJECT_ROOT):
        logger.error(f"仓库路径 {PROJECT_ROOT} 不存在或不是一个目录。")
        sys.exit(1)
    if FIND_CODE_SNIPPET.get('match') is not None:
        print('find_code start')
        logger.info("开始查找代码片段")
        find_code_snippet_main()
        print('find_code end')
        logger.info("查找代码片段结束")
    if FIND_SUFFIX.get('file_type') is not None:
        print('find_suffix start')
        logger.info("开始查找文件类型")
        find_suffix_main()
        print('find_suffix end')
        logger.info("查找文件类型结束")
