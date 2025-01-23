import pyautogui

def press_key(key):
    """
    按下按键。
    """
    try:
        pyautogui.press(key)
        return True
    except:
        return False

def input_key(text):
    """
    输入文本。
    """
    try:
        pyautogui.typewrite(text)
        return True
    except:
        return False
