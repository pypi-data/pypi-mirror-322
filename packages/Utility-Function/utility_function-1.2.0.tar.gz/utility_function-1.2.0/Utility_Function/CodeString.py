import base64

def base64_encode(text):
    """
    编码字符串为Base64。
    """
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def base64_decode(text):
    """
    解码Base64字符串。
    """
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')