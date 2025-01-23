import pyautogui

def get_screenshot():
    """
    获取屏幕截图。
    """
    try:
        screenshot = pyautogui.screenshot()
        return screenshot
    except:
        return None

def save_screenshot(path):
    """
    保存屏幕截图。
    """
    screenshot = get_screenshot()
    if screenshot is None:
        return False
    try:
        screenshot.save(path)
        return True
    except:
        return False
