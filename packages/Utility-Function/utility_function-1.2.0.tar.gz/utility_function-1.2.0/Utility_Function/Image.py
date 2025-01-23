import cv2

def show_image(window_name, image):
    """
    显示图像。
    """
    try:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    except:
        return False

def save_image(path, image):
    """
    保存图像。
    """
    try:
        cv2.imwrite(path, image)
        return True
    except:
        return False

def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    调整图像大小。
    """
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def rotate_image(image, angle, center=None, scale=1.0):
    """
    旋转图像。
    """
    (h, w) = image.shape[:2]
    center = center or (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(image, M, (w, h))

def flip_image(image, flip_code):
    """
    翻转图像。
    """
    return cv2.flip(image, flip_code)

def crop_image(image, x, y, w, h):
    """
    裁剪图像。
    """
    return image[y:y+h, x:x+w]
