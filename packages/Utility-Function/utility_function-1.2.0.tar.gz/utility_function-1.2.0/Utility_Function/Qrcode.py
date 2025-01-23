import cv2
from pyzbar import pyzbar

def QRcodescanner(path):
    frame = cv2.imread(path)
    if frame is None:
        return None

    decoded_objects = pyzbar.decode(frame)
    results = [obj.data.decode('utf-8') for obj in decoded_objects]

    if results:
        for item in results:
            print(item)
    else:
        print("未检测到二维码。")

    return results if results else None
