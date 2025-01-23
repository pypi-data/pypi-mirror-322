import random
import string

def random_string(length):
    """
    生成随机字符串。
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_number(length):
    """
    生成随机数字。
    """
    return ''.join(random.choices(string.digits, k=length))

def random_lower_string(length):
    """
    生成随机小写字母字符串。
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_upper_string(length):
    """
    生成随机大写字母字符串。
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def random_mix_string(length):
    """
    生成随机混合字母字符串。
    """
    return ''.join(random.choices(string.ascii_letters, k=length))

# 生成数字验证码
def createCode(who='有人', number=4, isreturn=True):
    code = ''.join(random.choices(string.digits, k=number))
    if isreturn:
        return code
    else:
        print(f"{who}向你发送验证码，验证码5分钟内有效，你的验证码为{code}")

# 验证码校验
def checkingCode(input_code, real_code):
    return input_code == real_code

# 生成字母加数字的验证码
def generate_verification_code(length=6, isreturn=True):
    code_chars = string.ascii_letters + string.digits
    code = ''.join(random.choices(code_chars, k=length))
    if isreturn:
        return code
    else:
        print(code)