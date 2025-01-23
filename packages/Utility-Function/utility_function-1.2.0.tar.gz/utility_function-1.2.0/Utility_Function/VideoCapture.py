import cv2

def open_camera(camera_index):
    """
    打开摄像头。
    """
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise Exception(f"无法打开摄像头{camera_index}")
        return cap
    except Exception:
        return None

def read_camera(cap):
    """
    读取摄像头。
    """
    try:
        ret, frame = cap.read()
        if not ret:
            raise Exception("读取摄像头失败")
        return frame
    except Exception:
        return None

def release_camera(cap):
    """
    释放摄像头。
    """
    if cap is not None:
        try:
            cap.release()
            cv2.destroyAllWindows()
            return True
        except Exception:
            return False
    return False

def save_camera_video(cap, path, fps=20):
    """
    保存摄像头视频。
    """
    if cap is None:
        return False

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, fps, (width, height))
        
        while True:
            frame = read_camera(cap)
            if frame is None:
                break
            out.write(frame)
        
        out.release()
        return True
    except Exception:
        return False
