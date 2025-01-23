import os
import shutil

def read_file(path):
    """
    读取文件内容。
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None


def write_file(path, content):
    """
    写入文件内容。
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except:
        return False


def append_file(path, content):
    """
    追加文件内容。
    """
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except:
        return False


def delete_file(path):
    """
    删除文件。
    """
    try:
        os.remove(path)
        return True
    except:
        return False


def rename_file(path, new_name):
    """
    重命名文件。
    """
    try:
        os.rename(path, new_name)
        return True
    except:
        return False


def copy_file(src_path, dst_path):
    """
    复制文件。
    """
    try:
        shutil.copyfile(src_path, dst_path)
        return True
    except:
        return False


def move_file(src_path, dst_path):
    """
    移动文件。
    """
    try:
        shutil.move(src_path, dst_path)
        return True
    except:
        return False


def get_file_size(path):
    """
    获取文件大小。
    """
    try:
        return os.path.getsize(path)
    except:
        return None


def get_file_list(dir_path):
    """
    获取目录下的文件列表。
    """
    try:
        return os.listdir(dir_path)
    except:
        return None


def create_dir(dir_path):
    """
    创建目录。
    """
    try:
        os.makedirs(dir_path)
        return True
    except:
        return False


def delete_dir(dir_path):
    """
    删除目录。
    """
    try:
        shutil.rmtree(dir_path)
        return True
    except:
        return False


def rename_dir(dir_path, new_name):
    """
    重命名目录。
    """
    try:
        os.rename(dir_path, new_name)
        return True
    except:
        return False


def copy_dir(src_path, dst_path):
    """
    复制目录。
    """
    try:
        shutil.copytree(src_path, dst_path)
        return True
    except:
        return False


def move_dir(src_path, dst_path):
    """
    移动目录。
    """
    try:
        shutil.move(src_path, dst_path)
        return True
    except:
        return False
