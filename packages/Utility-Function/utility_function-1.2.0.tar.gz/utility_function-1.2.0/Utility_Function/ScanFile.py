import os
import time

def scan_files_in_path(path):
    """
    扫描指定路径下的所有文件，并返回文件名列表。
    """
    if not os.path.exists(path):
        return []

    return [os.path.join(root, file) for root, _, files in os.walk(path) for file in files]

def use_scan_files_in_path(path, time_delay=0):
    files = scan_files_in_path(path)
    for file in files:
        print(file)
        time.sleep(time_delay)
    print(f"共扫描到{len(files)}个文件")
