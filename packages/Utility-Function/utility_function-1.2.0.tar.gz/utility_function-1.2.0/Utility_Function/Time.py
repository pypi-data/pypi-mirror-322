import datetime

def get_now_date():
    """
    获取当前日期，格式为 yyyy-mm-dd。
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_now_time():
    """
    获取当前时间，格式为 hh:mm:ss。
    """
    return datetime.datetime.now().strftime('%H:%M:%S')
    
def get_now_datetime():
    """
    获取当前日期和时间，格式为 yyyy-mm-dd hh:mm:ss。
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
