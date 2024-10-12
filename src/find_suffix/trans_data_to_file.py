import time
from shared.markdown_to_pdf import markdown_to_pdf
from shared.utils import get_root_path


def trans_data_to_file(data_arr):
    print(data_arr)
    content = ''
    for item in data_arr:
        total = 0
        file_type_content = f'\n## 文件后缀: {item.get("file_type")}'
        file_type_content += '\n| 文件目录 | 文件数量 | 文件列表 |\n| --- | --- | --- |'
        for k, v in item.get("group").items():
            if v is not None and len(v) > 0:
                suffix_file_list = ''
                for suffix_file in v:
                    suffix_file_list += f'<p>{suffix_file}</p>'
                suffix_file_list_len = len(v)
                total += suffix_file_list_len
                file_type_content += f'\n| {k} | {suffix_file_list_len} | {suffix_file_list} |'
        file_type_content = file_type_content.replace('## 文件后缀:', f'## 文件后缀:  total: {total}')
        content += file_type_content + '\n'
    # # 时间格式化
    create_time = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    file_absolutely_path = '/docs/find_suffix/' + create_time + '.pdf'
    target_file_path = get_root_path() + file_absolutely_path
    markdown_to_pdf_result = markdown_to_pdf(content, target_file_path)
    if markdown_to_pdf_result is False:
        raise ValueError('生成 pdf 失败')
    return {"file_absolutely_path": file_absolutely_path, "create_time": create_time}
