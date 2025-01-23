import hashlib

def hash_text(text, hash_function):
    """
    计算字符串的哈希值。
    :param text: 输入字符串
    :param hash_function: 哈希函数对象，例如 hashlib.md5
    :return: 哈希值的十六进制字符串表示
    """
    return hash_function(text.encode('utf-8')).hexdigest()

def md5(text):
    """
    计算字符串的MD5值。
    """
    return hash_text(text, hashlib.md5)

def sha1(text):
    """
    计算字符串的SHA1值。
    """
    return hash_text(text, hashlib.sha1)

def sha256(text):
    """
    计算字符串的SHA256值。
    """
    return hash_text(text, hashlib.sha256)

def sha512(text):
    """
    计算字符串的SHA512值。
    """
    return hash_text(text, hashlib.sha512)
