import subprocess

def run_command(command):
    """
    执行系统命令。
    """
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except Exception:
        return False

def run_command_with_output(command):
    """
    执行系统命令，并返回输出。
    """
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except Exception:
        return None

def run_command_with_input(command, input_str):
    """
    执行系统命令，并输入输入内容。
    """
    try:
        subprocess.run(command, input=input_str, shell=True, text=True, check=True)
        return True
    except Exception:
        return False

def run_command_with_input_and_output(command, input_str):
    """
    执行系统命令，并输入输入内容，并返回输出。
    """
    try:
        output = subprocess.check_output(command, input=input_str, shell=True, text=True)
        return output
    except Exception:
        return None
