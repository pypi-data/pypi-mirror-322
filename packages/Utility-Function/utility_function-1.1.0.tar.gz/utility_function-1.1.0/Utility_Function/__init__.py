import base64
import pyautogui
import hashlib
import platform
import random
import shutil
import datetime
import string
import os
import PIL
import cv2
import requests
import pyzbar.pyzbar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode
import time
import pyperclip
import subprocess
import socket
import pyaudio
import wave

class CAPTCHA:
    class String:
        @staticmethod
        def random_string(length):
            """
            生成随机字符串。
            """
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        @staticmethod
        def random_number(length):
            """
            生成随机数字。
            """
            return ''.join(random.choices(string.digits, k=length))

        @staticmethod
        def random_lower_string(length):
            """
            生成随机小写字母字符串。
            """
            return ''.join(random.choices(string.ascii_lowercase, k=length))

        @staticmethod
        def random_upper_string(length):
            """
            生成随机大写字母字符串。
            """
            return ''.join(random.choices(string.ascii_uppercase, k=length))

        @staticmethod
        def random_mix_string(length):
            """
            生成随机混合字母字符串。
            """
            return ''.join(random.choices(string.ascii_letters, k=length))

    class Number:
        # 生成数字验证码
        @staticmethod
        def createCode(who='有人', number=4, isreturn=True):
            code = ''.join(random.choices(string.digits, k=number))
            if isreturn:
                return code
            else:
                print(f"{who}向你发送验证码，验证码5分钟内有效，你的验证码为{code}")

        # 验证码校验
        @staticmethod
        def checkingCode(input_code, real_code):
            return input_code == real_code

        # 生成字母加数字的验证码
        @staticmethod
        def generate_verification_code(length=6, isreturn=True):
            code_chars = string.ascii_letters + string.digits
            code = ''.join(random.choices(code_chars, k=length))
            if isreturn:
                return code
            else:
                print(code)

class GraytoChar:
    @staticmethod
    def __GraytoChar(gray, chars):
        rate = gray / 256
        return chars[int(len(chars) * rate)]

    @staticmethod
    def UseGraytoChar(path, chars):
        try:
            img = PIL.Image.open(path).resize((60, 60)).convert('L')
        except Exception as e:
            print(f"无法加载图像，请检查路径是否正确。错误信息：{e}")
            return

        text = "\n".join("".join(GraytoChar.__GraytoChar(img.getpixel((i, j)), chars) for j in range(60)) for i in range(60))
        print(text)

        try:
            with open("output.txt", "w") as result:
                result.write(text)
            os.system("notepad output.txt")
        except Exception as e:
            print(f"文件操作失败：{e}")

class Email:
    def __init__(self, email, subject, sendto, password, zhenwen, smtp_server, port):
        self.smtp_server = smtp_server
        self.email = email
        self.subject = subject
        self.sendto = sendto
        self.password = password
        self.zhenwen = zhenwen
        self.port = port

    def send_email(self):
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.email, self.password)

            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = self.sendto
            message["Subject"] = self.subject
            message.attach(MIMEText(self.zhenwen, "plain"))

            server.sendmail(self.email, self.sendto, message.as_string())
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败: {e}")
        finally:
            server.quit()

class QrCode:
    @staticmethod
    def QRCodeGenerator(data, path):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(path + ".png")
        except Exception as e:
            print(f"生成二维码失败: {e}")

    @staticmethod
    def QRcodescanner(path):
        try:
            frame = cv2.imread(path)
        except Exception as e:
            print(f"无法加载图像，请检查路径是否正确。错误信息：{e}")
            return

        if frame is None:
            print("无法加载图像，请检查路径是否正确。")
        else:
            decoded_objects = pyzbar.pyzbar.decode(frame)
            results = [obj.data.decode('utf-8') for obj in decoded_objects]

            if results:
                print("扫描结果如下：")
                for item in results:
                    print(item)
            else:
                print("未检测到二维码。")

class NetworkUtility:   
    def get_local_ip_address():
        """
        获取本地IP地址。
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"获取本地IP地址失败：{e}")
            return None
    class IPv4:
        @staticmethod
        def IPv4_to_decimal(ip_address):
            """
            将一个IPv4地址转换为十进制格式。
            """
            return sum(int(octet) * (256 ** (3 - index)) for index, octet in enumerate(ip_address.split('.')))

        @staticmethod
        def decimal_to_IPv4(decimal_value):
            """
            将一个十进制值转换为IPv4地址。
            """
            return '.'.join(str(decimal_value >> (8 * (3 - index)) & 0xFF) for index in range(4))

    class IPv6:
        @staticmethod
        def IPv6_to_decimal(ip_address):
            """
            将一个IPv6地址转换为十进制格式。
            """
            return sum(int(hextet, 16) * (2 ** (16 * (7 - index))) for index, hextet in enumerate(ip_address.split(':')))

        @staticmethod
        def decimal_to_IPv6(decimal_value):
            """
            将一个十进制值转换为IPv6地址。
            """
            return ':'.join(format(decimal_value >> (16 * (7 - index)) & 0xFFFF, 'x') for index in range(8))

class BaseConversion:
    class HexDecimal:
        @staticmethod
        def hex_to_decimal(hex_value):
            """
            将一个十六进制值转换为十进制格式。
            """
            return int(hex_value, 16)

        @staticmethod
        def decimal_to_hex(decimal_value):
            """
            将一个十进制值转换为十六进制格式。
            """
            return format(decimal_value, 'x')

    class BinaryDecimal:
        @staticmethod
        def decimal_to_binary(decimal_value):
            """
            将一个十进制值转换为二进制格式。
            """
            return bin(decimal_value)[2:] if decimal_value else "0"

        @staticmethod
        def binary_to_decimal(binary_value):
            """
            将一个二进制值转换为十进制格式。
            """
            return int(binary_value, 2)

class Time:
    @staticmethod
    def get_now_date():
        """
        获取当前日期，格式为 yyyy-mm-dd。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_now_time():
        """
        获取当前时间，格式为 hh:mm:ss。
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    @staticmethod
    def get_now_datetime():
        """
        获取当前日期和时间，格式为 yyyy-mm-dd hh:mm:ss。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class File:
    class file:
        @staticmethod
        def read_file(path):
            """
            读取文件内容。
            """
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"文件读取失败：{e}")
                return None

        @staticmethod
        def write_file(path, content):
            """
            写入文件内容。
            """
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception as e:
                print(f"文件写入失败：{e}")
                return False

        @staticmethod
        def append_file(path, content):
            """
            追加文件内容。
            """
            try:
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception as e:
                print(f"文件追加失败：{e}")
                return False

        @staticmethod
        def delete_file(path):
            """
            删除文件。
            """
            try:
                os.remove(path)
                return True
            except Exception as e:
                print(f"文件删除失败：{e}")
                return False

        @staticmethod
        def rename_file(path, new_name):
            """
            重命名文件。
            """
            try:
                os.rename(path, new_name)
                return True
            except Exception as e:
                print(f"文件重命名失败：{e}")
                return False

        @staticmethod
        def copy_file(src_path, dst_path):
            """
            复制文件。
            """
            try:
                shutil.copyfile(src_path, dst_path)
                return True
            except Exception as e:
                print(f"文件复制失败：{e}")
                return False

        @staticmethod
        def move_file(src_path, dst_path):
            """
            移动文件。
            """
            try:
                shutil.move(src_path, dst_path)
                return True
            except Exception as e:
                print(f"文件移动失败：{e}")
                return False

        @staticmethod
        def get_file_size(path):
            """
            获取文件大小。
            """
            try:
                return os.path.getsize(path)
            except Exception as e:
                print(f"获取文件大小失败：{e}")
                return None

        @staticmethod
        def get_file_list(dir_path):
            """
            获取目录下的文件列表。
            """
            try:
                return os.listdir(dir_path)
            except Exception as e:
                print(f"获取文件列表失败：{e}")
                return None

    class dir:
        @staticmethod
        def create_dir(dir_path):
            """
            创建目录。
            """
            try:
                os.makedirs(dir_path)
                return True
            except Exception as e:
                print(f"目录创建失败：{e}")
                return False

        @staticmethod
        def delete_dir(dir_path):
            """
            删除目录。
            """
            try:
                shutil.rmtree(dir_path)
                return True
            except Exception as e:
                print(f"目录删除失败：{e}")
                return False

        @staticmethod
        def rename_dir(dir_path, new_name):
            """
            重命名目录。
            """
            try:
                os.rename(dir_path, new_name)
                return True
            except Exception as e:
                print(f"目录重命名失败：{e}")
                return False

        @staticmethod
        def copy_dir(src_path, dst_path):
            """
            复制目录。
            """
            try:
                shutil.copytree(src_path, dst_path)
                return True
            except Exception as e:
                print(f"目录复制失败：{e}")
                return False

        @staticmethod
        def move_dir(src_path, dst_path):
            """
            移动目录。
            """
            try:
                shutil.move(src_path, dst_path)
                return True
            except Exception as e:
                print(f"目录移动失败：{e}")
                return False

class Image:
    @staticmethod
    def show_image(window_name, image):
        """
        显示图像。
        """
        try:
            cv2.imshow(window_name, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            print(f"显示图像失败：{e}")
            return False

    @staticmethod
    def save_image(path, image):
        """
        保存图像。
        """
        try:
            cv2.imwrite(path, image)
            return True
        except Exception as e:
            print(f"保存图像失败：{e}")
            return False

    @staticmethod
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

    @staticmethod
    def rotate_image(image, angle, center=None, scale=1.0):
        """
        旋转图像。
        """
        (h, w) = image.shape[:2]
        center = center or (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        return cv2.warpAffine(image, M, (w, h))

    @staticmethod
    def flip_image(image, flip_code):
        """
        翻转图像。
        """
        return cv2.flip(image, flip_code)

    @staticmethod
    def crop_image(image, x, y, w, h):
        """
        裁剪图像。
        """
        return image[y:y+h, x:x+w]

class Video:
    @staticmethod
    def read_video(path):
        """
        读取视频。
        """
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"无法打开视频文件：{path}")
            return None

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def save_video(path, frames):
        """
        保存视频。
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, 20.0, (640, 480))

        for frame in frames:
            out.write(frame)

        out.release()
        return True

    @staticmethod
    def show_video(window_name, path):
        """
        显示视频。
        """
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"无法打开视频文件：{path}")
            return False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return True

class Web:
    @staticmethod
    def get_html(url):
        """
        获取网页HTML内容。
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"获取网页HTML内容失败：{e}")
            return None

    @staticmethod
    def get_json(url):
        """
        获取网页JSON内容。
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取网页JSON内容失败：{e}")
            return None

    @staticmethod
    def get_image(url):
        """
        获取网页图片。
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"获取网页图片失败：{e}")
            return None

    @staticmethod
    def post_data(url, data):
        """
        向网页提交数据。
        """
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"提交数据失败：{e}")
            return None

    @staticmethod
    def download_file(url, path):
        """
        下载文件。
        """
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            return True
        except requests.RequestException as e:
            print(f"文件下载失败：{e}")
            return False

    @staticmethod
    def upload_file(url, path):
        """
        上传文件。
        """
        try:
            with open(path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"文件上传失败：{e}")
            return None

class System:
    @staticmethod
    def get_platform():
        """
        获取当前平台。
        """
        return platform.system()

    @staticmethod
    def get_platform_version():
        """
        获取当前平台版本。
        """
        return platform.version()

    @staticmethod
    def get_platform_release():
        """
        获取当前平台发行版本。
        """
        return platform.release()

    @staticmethod
    def get_platform_machine():
        """
        获取当前平台架构。
        """
        return platform.machine()

    @staticmethod
    def get_platform_processor():
        """
        获取当前平台处理器。
        """
        return platform.processor()

    @staticmethod
    def get_python_version():
        """
        获取当前Python版本。
        """
        return platform.python_version()

    @staticmethod
    def get_python_build():
        """
        获取当前Python编译版本。
        """
        return platform.python_build()

    @staticmethod
    def get_python_compiler():
        """
        获取当前Python编译器。
        """
        return platform.python_compiler()

    @staticmethod
    def get_python_branch():
        """
        获取当前Python分支。
        """
        return platform.python_branch()

    @staticmethod
    def get_python_implementation():
        """
        获取当前Python实现。
        """
        return platform.python_implementation()

    @staticmethod
    def get_python_revision():
        """
        获取当前Python修订版本。
        """
        return platform.python_revision()

    @staticmethod
    def get_system_version():
        """
        获取当前系统版本。
        """
        return platform.system_alias(platform.system(), platform.release(), platform.version())

    @staticmethod
    def get_system_name():
        """
        获取当前系统名称。
        """
        return platform.system()

    @staticmethod
    def get_system_release():
        """
        获取当前系统发行版本。
        """
        return platform.release()

    @staticmethod
    def get_system_architecture():
        """
        获取当前系统架构。
        """
        return platform.architecture()

    @staticmethod
    def get_system_uname():
        """
        获取当前系统uname信息。
        """
        return platform.uname()

    @staticmethod
    def get_system_libc_version():
        """
        获取当前系统libc版本。
        """
        return platform.libc_ver()

    @staticmethod
    def get_system_mac_ver():
        """
        获取当前系统mac版本。
        """
        return platform.mac_ver()

    @staticmethod
    def get_system_win32_ver():
        """
        获取当前系统win32版本。
        """
        return platform.win32_ver()

    @staticmethod
    def get_system_win32_edition():
        """
        获取当前系统win32版本。
        """
        return platform.win32_edition()

    @staticmethod
    def get_system_win32_is_iot():
        """
        获取当前系统是否为IOT。
        """
        return platform.win32_is_iot()

    @staticmethod
    def get_system_win32_ver_major():
        """
        获取当前系统win32版本主版本号。
        """
        return platform.win32_ver()[0]

    @staticmethod
    def get_system_win32_ver_minor():
        """
        获取当前系统win32版本次版本号。
        """
        return platform.win32_ver()[1]

    @staticmethod
    def get_system_win32_ver_build():
        """
        获取当前系统win32版本构建号。
        """
        return platform.win32_ver()[2]

    @staticmethod
    def get_system_win32_ver_platform():
        """
        获取当前系统win32版本平台。
        """
        return platform.win32_ver()[3]

    @staticmethod
    def get_system_win32_ver_service_pack():
        """
        获取当前系统win32版本服务包。
        """
        return platform.win32_ver()[4]

    @staticmethod
    def get_system_win32_ver_product_type():
        """
        获取当前系统win32版本产品类型。
        """
        return platform.win32_ver()[5]

class HashValueString:
    @staticmethod
    def md5(text):
        """
        计算字符串的MD5值。
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha1(text):
        """
        计算字符串的SHA1值。
        """
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha256(text):
        """
        计算字符串的SHA256值。
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha512(text):
        """
        计算字符串的SHA512值。
        """
        return hashlib.sha512(text.encode('utf-8')).hexdigest()

class CodeString:
    @staticmethod
    def base64_encode(text):
        """
        编码字符串为Base64。
        """
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_decode(text):
        """
        解码Base64字符串。
        """
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')

class ScanFile:
    @staticmethod
    def __scan_files_in_path(path):
        """
        扫描指定路径下的所有文件，并返回文件名列表。
        """
        if not os.path.exists(path):
            print(f"路径{path}不存在")
            return []

        print(f"开始扫描")
        return [os.path.join(root, file) for root, _, files in os.walk(path) for file in files]

    def use_scan_files_in_path(self, path, time_delay=0):
        files = ScanFile.__scan_files_in_path(path)
        for file in files:
            print(file)
            time.sleep(time_delay)
        print(f"共扫描到{len(files)}个文件")

class KeyBoard:
    @staticmethod
    def press_key(key):
        """
        按下按键。
        """
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"按键按下失败：{e}")
            return False

    @staticmethod
    def input_key(text):
        """
        输入按键。
        """
        try:
            pyautogui.typewrite(text)
            return True
        except Exception as e:
            print(f"输入按键失败：{e}")
            return False

class Mouse:
    @staticmethod
    def click_left_button():
        """
        点击鼠标左键。
        """
        try:
            pyautogui.click()
            return True
        except Exception as e:
            print(f"点击左键失败：{e}")
            return False

    @staticmethod
    def click_right_button():
        """
        点击鼠标右键。
        """
        try:
            pyautogui.click(button='right')
            return True
        except Exception as e:
            print(f"点击右键失败：{e}")
            return False

    @staticmethod
    def move_to_position(x, y):
        """
        移动鼠标到指定位置。
        """
        try:
            pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            print(f"移动鼠标失败：{e}")
            return False

    @staticmethod
    def move_to_position_with_duration(x, y, duration):
        """
        移动鼠标到指定位置，持续指定时间。
        """
        try:
            pyautogui.moveTo(x, y, duration)
            return True
        except Exception as e:
            print(f"移动鼠标失败：{e}")
            return False

    @staticmethod
    def move_to_position_with_duration_and_tween(x, y, duration, tween):
        """
        移动鼠标到指定位置，持续指定时间，使用缓动效果。
        """
        try:
            pyautogui.moveTo(x, y, duration, tween)
            return True
        except Exception as e:
            print(f"移动鼠标失败：{e}")
            return False

class ScreenShot:
    @staticmethod
    def get_screenshot():
        """
        获取屏幕截图。
        """
        return pyautogui.screenshot()

    @staticmethod
    def save_screenshot(path):
        """
        保存屏幕截图。
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            return True
        except Exception as e:
            print(f"保存截图失败：{e}")
            return False

class ClipBoard:
    @staticmethod
    def get_clipboard():
        """
        获取剪贴板内容。
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"获取剪贴板内容失败：{e}")
            return None

    @staticmethod
    def set_clipboard(text):
        """
        设置剪贴板内容。
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"设置剪贴板内容失败：{e}")
            return False

class Process:
    @staticmethod
    def run_command(command):
        """
        执行系统命令。
        """
        try:
            os.system(command)
            return True
        except Exception as e:
            print(f"执行命令失败：{e}")
            return False

    @staticmethod
    def run_command_with_output(command):
        """
        执行系统命令，并返回输出。
        """
        try:
            output = subprocess.check_output(command, shell=True)
            return output.decode('utf-8')
        except Exception as e:
            print(f"执行命令并获取输出失败：{e}")
            return None

    @staticmethod
    def run_command_with_input(command, input_str):
        """
        执行系统命令，并输入输入内容。
        """
        try:
            subprocess.run(command, input=input_str.encode('utf-8'), shell=True)
            return True
        except Exception as e:
            print(f"执行命令并输入内容失败：{e}")
            return False

    @staticmethod
    def run_command_with_input_and_output(command, input_str):
        """
        执行系统命令，并输入输入内容，并返回输出。
        """
        try:
            output = subprocess.check_output(command, input=input_str.encode('utf-8'), shell=True)
            return output.decode('utf-8')
        except Exception as e:
            print(f"执行命令并获取输出失败：{e}")
            return None

class VideoCapture:
    @staticmethod
    def open_camera(camera_index):
        """
        打开摄像头。
        """
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                print(f"无法打开摄像头{camera_index}")
                return None
            return cap
        except Exception as e:
            print(f"打开摄像头失败：{e}")
            return None

    @staticmethod
    def read_camera(cap):
        """
        读取摄像头。
        """
        ret, frame = cap.read()
        if not ret:
            print(f"读取摄像头失败")
            return None
        return frame

    @staticmethod
    def release_camera(cap):
        """
        释放摄像头。
        """
        cap.release()
        cv2.destroyAllWindows()
        return True

    @staticmethod
    def save_camera_video(cap, path, fps=20):
        """
        保存摄像头视频。
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, fps, (640, 480))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

                out.write(frame)

        out.release()
        return True         
    
class AudioCapture:
    def __init__(self, filename, rate=44100, chunk=1024, channels=1, format=pyaudio.paInt16):
        self.filename = filename
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format = format

    def record(self, duration):
        """
        录制指定时长的音频。
        :param duration: 录制时长，单位为秒。
        """
        audio = pyaudio.PyAudio()

        # 打开音频流
        stream = audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)

        print("正在录音...")

        frames = []

        # 录制音频数据
        for _ in range(0, int(self.rate / self.chunk * duration + 1)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("录音结束")

        # 关闭音频流
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 保存音频数据到文件
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        return self.filename

print("欢迎使用Utility_Function辅助工具")
print("Welcome to the Utility_Function helper")
