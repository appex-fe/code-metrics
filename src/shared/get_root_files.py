import os


# 读取根目录下所有的文件，返回文件的路径和文件类型
# 如果有文件夹的话，递归读取文件夹下的文件
def read_all_files(project_root_dir):
    file_list = []
    for root, dirs, files in os.walk(project_root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_type = file_path.split('.')[-1]
            file_list.append((file_path, file_type))
    return file_list
