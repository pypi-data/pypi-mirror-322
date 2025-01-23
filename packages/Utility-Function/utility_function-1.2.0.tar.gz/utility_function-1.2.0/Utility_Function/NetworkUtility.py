import socket

def get_local_ip_address():
    try:
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        for ip in ip_addresses:
            if not ip.startswith('127.'):
                return ip
        # 如果没有找到非回环地址，返回第一个IP地址
        return ip_addresses[0]
    except:
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
