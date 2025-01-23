import cv2

def read_video(path):
    """
    读取视频。
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
    finally:
        cap.release()
        cv2.destroyAllWindows()

def save_video(path, frames, fps=20.0, frame_size=(640, 480)):
    """
    保存视频。
    """
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path, fourcc, fps, frame_size)

    try:
        for frame in frames:
            out.write(frame)
    finally:
        out.release()

def show_video(window_name, path):
    """
    显示视频。
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return True
