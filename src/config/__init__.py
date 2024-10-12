import json
from shared.utils import get_root_path

# 方法一：使用相对路径
with open(get_root_path() + '/config.json', 'r', encoding='utf-8') as file:
    config_data = json.load(file)

if config_data is None:
    raise ValueError('配置文件不存在')

PROJECT_ROOT: str = "/app/project"

PROJECT_ROOT_DIR: str = PROJECT_ROOT + f"/{config_data['PROJECT_ROOT_DIR']}" if config_data.get(
    'PROJECT_ROOT_DIR') else ''

IS_CONFIG_DINGTALK: bool = (config_data['ding_talk']
                            and config_data['ding_talk']['token']
                            and config_data['ding_talk']['secret'])

DING_TALK = {
    'token': config_data.get('ding_talk', {}).get('token'),
    'secret': config_data.get('ding_talk', {}).get('secret')
}

FIND_CODE_SNIPPET = {
    'match': config_data.get('code_snippets', {}).get('match'),
    'ignore_dir': config_data.get('code_snippets', {}).get('ignore_dir')
}

FIND_SUFFIX = {
    'file_type': config_data.get('find_suffix', {}).get('file_type'),
    'group_by': config_data.get('find_suffix', {}).get('group_by'),
    'ignore_dir': config_data.get('find_suffix', {}).get('ignore_dir')
}

DOCS_HOST_PORT = config_data.get('docs_host_port')
