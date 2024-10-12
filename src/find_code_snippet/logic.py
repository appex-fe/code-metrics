from config import PROJECT_ROOT_DIR


# 将文件路径改为相对路径
def change_file_path(file_path):
    return file_path.replace(PROJECT_ROOT_DIR, '')


# 根据代码片段将结果进行聚合
# 输出数据格式为 {code_snippet: [(file_path, code_snippet_count, code_snippet_lines)]}
# 如果该代码片段对应的文件路径中统计到的代码片段次数为0，则不进行输出
def aggregate_code_snippet(result):
    code_snippet_aggregate = {}
    for path, item_result in result.items():
        for code_snippet, code_snippet_count in item_result['code_snippet_count'].items():
            if code_snippet_count > 0:
                if code_snippet not in code_snippet_aggregate:
                    code_snippet_aggregate[code_snippet] = []
                code_snippet_aggregate[code_snippet].append({
                    'file_path': change_file_path(path),
                    'code_snippet_count': code_snippet_count,
                    'code_snippet_lines': item_result['code_snippet_lines'][code_snippet]
                })
    return code_snippet_aggregate


# 将 数组对象转换为 markdown 表格形式
def transform_array_to_markdown_table(array):
    markdown_context = '\n'
    markdown_context += "| 文件路径 | 代码片段次数 | 代码所在行数 |\n"
    markdown_context += "| --- | --- | --- |\n"
    for item in array:
        markdown_context += (f"| {item['file_path']} | "
                             f"{item['code_snippet_count']} | "
                             f"{','.join(map(str, item['code_snippet_lines']))} |"
                             f"\n")
    return markdown_context


# 遍历循环字典对象，根据字典的key 生成 markdown 表格
def transform_dict_to_markdown_table(dict_obj):
    markdown_context = ''
    for k, v in dict_obj.items():
        markdown_context += f'\n ## 代码片段: `{k}`\n'
        markdown_context += transform_array_to_markdown_table(v)
    return markdown_context
