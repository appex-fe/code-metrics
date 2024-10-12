from collections import defaultdict


def compare_json_data(data_json):
    if len(data_json) < 2:
        print("数据不足,无法比较")
        return

    last = data_json[-1]['data']
    previous = data_json[-2]['data']

    diff_changes = defaultdict(lambda: {'added': [], 'removed': [], 'code_snippet_count_changes': {}})

    for key in set(last.keys()) | set(previous.keys()):
        last_files = {item['file_path']: item for item in last.get(key, [])}
        prev_files = {item['file_path']: item for item in previous.get(key, [])}

        for file_path in set(last_files.keys()) | set(prev_files.keys()):
            if file_path in last_files and file_path not in prev_files:
                diff_changes[key]['added'].append(file_path)
            elif file_path not in last_files and file_path in prev_files:
                diff_changes[key]['removed'].append(file_path)
            elif last_files[file_path]['code_snippet_count'] != prev_files[file_path]['code_snippet_count']:
                diff_changes[key]['code_snippet_count_changes'][file_path] = {
                    'from': prev_files[file_path]['code_snippet_count'],
                    'to': last_files[file_path]['code_snippet_count']
                }

    return diff_changes


def export_changes(changes_content):
    diff_context = f"\n ## 代码片段: \n"
    for key, change in changes_content.items():
        diff_context += f"### {key}\n"
        if change['added']:
            diff_context += "  - 新增文件:\n"
            for file in change['added']:
                diff_context += f"    - {file}\n"
        if change['removed']:
            diff_context += " - 删除文件:\n"
            for file in change['removed']:
                diff_context += f"    - {file}\n"
        if change['code_snippet_count_changes']:
            diff_context += " - 代码片段变化:\n"
            for file, counts in change['code_snippet_count_changes'].items():
                diff_context += f"    - {file}: {counts['from']} -> {counts['to']}\n"
    return diff_context
