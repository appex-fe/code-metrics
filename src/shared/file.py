import os

from config import PROJECT_ROOT_DIR
from shared.logger import default_logger as logger


# 读取指定路径的文件内容
def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f'文件不存在: {file_path}')
        return '文件不存在'
    except Exception as e:
        logger.error(f'读取文件内容失败: {file_path} {e}')
        return '读取文件内容失败'


# 获取文件夹下第一层子文件夹
def get_first_layer_dir(dir_path):
    subdirectories = [name for name in os.listdir(dir_path)
                      if os.path.isdir(os.path.join(dir_path, name))]
    return subdirectories


def get_root_files(file_path):
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # JSON 配置文件的路径
    return os.path.join(current_dir, file_path)


# 读取目录下所有的文件，返回文件的路径和文件类型，如果是文件夹则递归读取文件夹下的文件
def find_all_files_in_dir(file_type, dir_path, ignore_dir):
    file_type_list = []
    for root, dirs, files in os.walk(dir_path):
        for math_type_file in files:
            file_path = os.path.join(root, math_type_file).replace(PROJECT_ROOT_DIR, '')
            # 如果 file_path 匹配到 find_suffix_ignore_dir 列表中任一项开头的，则跳过
            if any([file_path.startswith(ignore_dir_item) for ignore_dir_item in ignore_dir]):
                continue
            match_file_type = file_path.split('.')[-1]
            if match_file_type in file_type:
                file_type_list.append({'file_path': file_path, 'file_type': match_file_type})
    return file_type_list


# 判断文件是否有写入权限
def is_writable(file_path):
    return os.access(file_path, os.W_OK)
