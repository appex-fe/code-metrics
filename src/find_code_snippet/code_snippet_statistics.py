import time

from config import FIND_CODE_SNIPPET, PROJECT_ROOT_DIR
from find_code_snippet.match import count_code_snippet
from shared.markdown_to_pdf import markdown_to_pdf
from shared.file import read_file_content
from shared.get_root_files import read_all_files
from shared.utils import is_in_array, get_root_path
from find_code_snippet.logic import aggregate_code_snippet, transform_dict_to_markdown_table


def calculate_code_snippet(file_list, target_file_type, code_snippets):
    result = {}
    for file_path, file_type in file_list:
        if file_type in target_file_type and not is_in_array(file_path, FIND_CODE_SNIPPET.get('ignore_dir')):
            file_content = read_file_content(file_path)
            code_snippet_count_num, code_snippet_lines = count_code_snippet(file_content, code_snippets)
            result[file_path] = {'code_snippet_count': code_snippet_count_num, 'code_snippet_lines': code_snippet_lines}
    return result


def statistics_code_snippet():
    file_list = read_all_files(PROJECT_ROOT_DIR)
    for match_rule in FIND_CODE_SNIPPET.get('match'):
        code_snippet_result = calculate_code_snippet(file_list, match_rule['file_type'], match_rule['code_snippets'])
        aggregate_data = aggregate_code_snippet(code_snippet_result)
        report_context = transform_dict_to_markdown_table(aggregate_data)
        create_time = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
        file_absolutely_path = '/docs/find_code_snippet/' + create_time + '.pdf'
        target_file_path = get_root_path() + file_absolutely_path
        markdown_to_pdf_result = markdown_to_pdf(report_context, target_file_path)
        if markdown_to_pdf_result is False:
            raise ValueError('生成 pdf 失败')
        return {"file_absolutely_path": file_absolutely_path, "create_time": create_time}
