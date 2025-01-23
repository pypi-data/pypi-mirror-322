import platform

def get_platform():
    """
    获取当前平台。
    """
    return platform.system()

def get_platform_version():
    """
    获取当前平台版本。
    """
    return platform.version()

def get_platform_release():
    """
    获取当前平台发行版本。
    """
    return platform.release()

def get_platform_machine():
    """
    获取当前平台架构。
    """
    return platform.machine()

def get_platform_processor():
    """
    获取当前平台处理器。
    """
    return platform.processor()

def get_python_version():
    """
    获取当前Python版本。
    """
    return platform.python_version()

def get_python_build():
    """
    获取当前Python编译版本。
    """
    return platform.python_build()

def get_python_compiler():
    """
    获取当前Python编译器。
    """
    return platform.python_compiler()

def get_python_branch():
    """
    获取当前Python分支。
    """
    return platform.python_branch()

def get_python_implementation():
    """
    获取当前Python实现。
    """
    return platform.python_implementation()

def get_python_revision():
    """
    获取当前Python修订版本。
    """
    return platform.python_revision()

def get_system_version():
    """
    获取当前系统版本。
    """
    return platform.system_alias(platform.system(), platform.release(), platform.version())

def get_system_name():
    """
    获取当前系统名称。
    """
    return get_platform()

def get_system_release():
    """
    获取当前系统发行版本。
    """
    return get_platform_release()

def get_system_architecture():
    """
    获取当前系统架构。
    """
    return platform.architecture()[0]

def get_system_uname():
    """
    获取当前系统uname信息。
    """
    return platform.uname()

def get_system_libc_version():
    """
    获取当前系统libc版本。
    """
    return platform.libc_ver()[0]

def get_system_mac_ver():
    """
    获取当前系统mac版本。
    """
    return platform.mac_ver()[0]

def get_system_win32_ver():
    """
    获取当前系统win32版本。
    """
    return platform.win32_ver()

def get_system_win32_edition():
    """
    获取当前系统win32版本。
    """
    return platform.win32_edition()

def get_system_win32_is_iot():
    """
    获取当前系统是否为IOT。
    """
    return platform.win32_is_iot()

def get_system_win32_ver_major():
    """
    获取当前系统win32版本主版本号。
    """
    return platform.win32_ver()[0]

def get_system_win32_ver_minor():
    """
    获取当前系统win32版本次版本号。
    """
    return platform.win32_ver()[1]

def get_system_win32_ver_build():
    """
    获取当前系统win32版本构建号。
    """
    return platform.win32_ver()[2]

def get_system_win32_ver_platform():
    """
    获取当前系统win32版本平台。
    """
    return platform.win32_ver()[3]

def get_system_win32_ver_service_pack():
    """
    获取当前系统win32版本服务包。
    """
    return platform.win32_ver()[4]

def get_system_win32_ver_product_type():
    """
    获取当前系统win32版本产品类型。
    """
    return platform.win32_ver()[5]
