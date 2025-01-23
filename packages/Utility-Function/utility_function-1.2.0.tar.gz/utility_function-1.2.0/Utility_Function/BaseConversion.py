class HexDecimal:
    @staticmethod
    def hex_to_decimal(hex_value):
        #将一个十六进制值转换为十进制格式。
        
        return int(hex_value, 16)

    @staticmethod
    def decimal_to_hex(decimal_value):
        #将一个十进制值转换为十六进制格式。
        return format(decimal_value, 'x')

class BinaryDecimal:
    @staticmethod
    def decimal_to_binary(decimal_value):
        #将一个十进制值转换为二进制格式。
        return bin(decimal_value)[2:] if decimal_value else "0"
    
    @staticmethod
    def binary_to_decimal(binary_value):
        #将一个二进制值转换为十进制格式。
        return int(binary_value, 2)