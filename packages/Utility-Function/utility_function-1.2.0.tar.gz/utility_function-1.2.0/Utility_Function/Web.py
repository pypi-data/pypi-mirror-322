import requests

def get_html(url):
    """
    获取网页HTML内容。
    """
    return _get_content(url, content_type='text')

def get_json(url):
    """
    获取网页JSON内容。
    """
    return _get_content(url, content_type='json')

def get_image(url):
    """
    获取网页图片。
    """
    return _get_content(url, content_type='content', stream=True)

def post_data(url, data):
    """
    向网页提交数据。
    """
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.text
    except:
        return None

def download_file(url, path):
    """
    下载文件。
    """
    return _download_or_upload(url, path, mode='wb', action='download')

def upload_file(url, path):
    """
    上传文件。
    """
    return _download_or_upload(url, path, mode='rb', action='upload')

def _get_content(url, content_type='text', stream=False):
    """
    通用方法获取网页内容。
    """
    try:
        response = requests.get(url, stream=stream)
        response.raise_for_status()
        if content_type == 'text':
            return response.text
        elif content_type == 'json':
            return response.json()
        elif content_type == 'content':
            return response.content
    except:
        return None

def _download_or_upload(url, path, mode, action):
    """
    通用方法用于下载或上传文件。
    """
    try:
        if action == 'download':
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(path, mode) as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            return True
        elif action == 'upload':
            with open(path, mode) as file:
                files = {'file': file}
                response = requests.post(url, files=files)
                response.raise_for_status()
                return response.text
    except:
        return False
