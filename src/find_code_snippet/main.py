from config import DOCS_HOST_PORT
from shared.report_DingTalk import send_link_dingtalk
from shared.utils import get_root_path, create_dir_if_not_exists
from find_code_snippet.code_snippet_statistics import statistics_code_snippet
from shared.logger import default_logger as logger


def main():
    # 判断 docs 下有没有 find_suffix 文件夹，没有则创建
    create_dir_if_not_exists(get_root_path() + '/docs/find_code_snippet')
    logger.info("开始查找代码片段")
    trans_response = statistics_code_snippet()
    logger.info("查找代码片段结束")
    send_link_dingtalk('代码片段数统计', f'{trans_response.get("create_time")} vue 代码片段数统计',
                       f'{DOCS_HOST_PORT}{trans_response.get("file_absolutely_path")}')


if __name__ == '__main__':
    main()
