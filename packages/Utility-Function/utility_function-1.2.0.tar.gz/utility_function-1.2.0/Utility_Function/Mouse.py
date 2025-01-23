import pyautogui

def click_button(button='left'):
    """
    点击鼠标指定按钮。
    :param button: 按钮名称，默认为'left'，也可以是'right'。
    :return: 成功点击返回True，否则返回False。
    """
    try:
        pyautogui.click(button=button)
        return True
    except:
        return False

def move_to_position(x, y, duration=0, tween=None):
    """
    移动鼠标到指定位置，可选持续时间和缓动效果。
    :param x: 目标位置的x坐标。
    :param y: 目标位置的y坐标。
    :param duration: 移动持续时间，默认为0。
    :param tween: 缓动效果，默认为None。
    :return: 成功移动返回True，否则返回False。
    """
    try:
        pyautogui.moveTo(x, y, duration, tween)
        return True
    except:
        return False
