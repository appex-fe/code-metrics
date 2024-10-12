import re
from shared.utils import str_to_regex


# 统计文件内容中匹配到指定代码片段的次数，返回文件路径、代码片段次数、代码所在行数
# 代码片段有多个,返回的数据结构为: {code_snippet: (code_snippet_count, code_snippet_lines)}
def count_code_snippet(file_content, code_snippets):
    code_snippet_count_obj = {}
    code_snippet_lines = {}
    for code_snippet_item in code_snippets:
        code_snippet_count_obj[code_snippet_item] = 0
        code_snippet_lines[code_snippet_item] = []
    lines = file_content.split('\n')
    for i, line in enumerate(lines):
        for target_code_snippet in code_snippets:
            regx = str_to_regex(target_code_snippet)
            if regx is False and target_code_snippet in line:
                code_snippet_count_obj[target_code_snippet] += 1
                code_snippet_lines[target_code_snippet].append(i + 1)
            elif regx is not False:
                target_code_count = len(re.findall(regx, line))
                if target_code_count > 0:
                    code_snippet_count_obj[target_code_snippet] += target_code_count
                    code_snippet_lines[target_code_snippet].append(i + 1)
    return code_snippet_count_obj, code_snippet_lines
