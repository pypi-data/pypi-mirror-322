import pyperclip

def get_clipboard():
    """
    获取剪贴板内容。
    """
    try:
        return pyperclip.paste()
    except Exception:
        return None


def set_clipboard(text):
    """
    设置剪贴板内容。
    """
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False
