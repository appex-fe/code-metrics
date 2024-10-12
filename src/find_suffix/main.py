import os
from config import FIND_SUFFIX, PROJECT_ROOT_DIR, DOCS_HOST_PORT
from find_suffix.trans_data_to_file import trans_data_to_file
from shared.utils import create_dir_if_not_exists, get_root_path
from shared.file import get_first_layer_dir, find_all_files_in_dir
from shared.report_DingTalk import send_link_dingtalk
from shared.logger import default_logger as logger


# 根据 group_by 的配置，将文件夹下的文件进行分组
# FIND_SUFFIX.group_by 为项目文件夹下的文件类型进行分组
# 如果是 components/ 下的文件，返回的结果为 {'component': { "vue": ['components/xxx.vue']}}
# 如果是 views/* 下的文件，返回的结果为 {'views/site': { "vue": ['views/site/xxx.vue']}}
# 也就是说如果带有 * 的文件夹，会将该文件夹下第一层的文件夹作为 key 进行分组
def get_group_dir_key():
    group_dir_key = {}
    for group in FIND_SUFFIX.get('group_by'):
        if group.endswith('/*'):
            parent_dri = group.replace('/*', '')
            first_layer_dir = get_first_layer_dir(os.path.join(PROJECT_ROOT_DIR, parent_dri))
            for first_layer_dir_item in first_layer_dir:
                group_dir_key[parent_dri + '/' + first_layer_dir_item] = []
        else:
            group_dir_key[group] = []
    return group_dir_key


def find_all_files_in_dir_group_by_suffix(dir_path):
    suffix_group = []
    group_dir_key = get_group_dir_key()
    for file_type_item in FIND_SUFFIX.get('file_type'):
        file_lists = find_all_files_in_dir([file_type_item], dir_path, FIND_SUFFIX.get('ignore_dir'))
        group_dir_key_for_file_type = {key: value.copy() for key, value in group_dir_key.items()}
        for file_item in file_lists:
            for group in group_dir_key:
                if file_item.get('file_path').startswith(group):
                    group_dir_key_for_file_type[group].append(file_item.get('file_path'))
        suffix_group.append({"file_type": file_type_item, "group": group_dir_key_for_file_type})
    return suffix_group


def main():
    # 判断 docs 下有没有 find_suffix 文件夹，没有则创建
    create_dir_if_not_exists(get_root_path() + '/docs/find_suffix')
    logger.info("开始查找文件类型")
    result = find_all_files_in_dir_group_by_suffix(PROJECT_ROOT_DIR)
    trans_response = trans_data_to_file(result)
    logger.info("查找文件类型结束")
    send_link_dingtalk('文件类型统计', f'{trans_response.get("create_time")} vue 文件类型统计',
                       f'{DOCS_HOST_PORT}{trans_response.get("file_absolutely_path")}')


if __name__ == '__main__':
    main()
