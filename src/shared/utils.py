import json
import re
import os


def is_in_array(string, array):
    for item in array:
        if item in string:
            return True
    return False


# 读取JSON 文件
# 如果文件不存在则返回None
def load_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


# 判断字符串是否是正则表达式 如果是则返回正则表达式对象，否则返回False
def str_to_regex(string):
    # 匹配以斜杠开始，以斜杠结束，可能跟随一些标志的模式
    pattern = r'^/(.+)/([gimsuy]*)$'
    match = re.match(pattern, string)
    if match:
        # 提取正则表达式主体和标志
        regex_body, flags_str = match.groups()
        # 转换标志
        flags = 0
        if 'i' in flags_str:
            flags |= re.IGNORECASE
        if 'm' in flags_str:
            flags |= re.MULTILINE
        if 's' in flags_str:
            flags |= re.DOTALL

        # 检查正则表达式主体是否有效
        try:
            return re.compile(regex_body, flags)
        except re.error:
            return False

    return False


# 如果 docs 下没有指定的文件夹，则创建
def create_dir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


# 获取 src 的根目录地址
def get_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
