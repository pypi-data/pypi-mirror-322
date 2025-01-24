import os
import sys
import ctypes
import shutil
import hashlib
import platform
import subprocess
import re
from . import main

def desktop():
    """获取桌面位置(\Desktop)"""
    home_directory = os.path.expanduser("~")

    return os.path.join(home_directory, "Desktop")

def username():
    """获取用户名"""

    if platform.system() == "Windows":
        return os.getenv("USERNAME")

    else:
        return os.getenv("USER")

def route(relative_path):
    """
    从相对路径获取绝对路径
    relative_path:相对路径
    """
    # 检查该路径是否存在
    if os.path.exists(relative_path):
        print("该路径存在。")
    else:
        print("该路径不存在。")

    # 获取对应的绝对路径
    return os.path.abspath(relative_path)

def calculate_hash(file_path):
    """
    计算给定文件的 SHA256 哈希值
    file_path:文件路径
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # 按块读取文件内容以避免占用大量内存
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_sha256.update(byte_block)
            
    return hash_sha256.hexdigest()

def copy(source_file,destination_file):
    """
    复制文件
    source_file:源文件路径,例如 "C:/path/to/source.txt"
    destination_file:目标文件路径,例如 "C:/path/to/destination.txt"
    """
    try:

        with open(source_file, 'rb') as src:
            content = src.read()
            
        with open(destination_file, 'wb') as dest:
            dest.write(content)
        
    except FileNotFoundError:
        print("源文件不存在:", source_file)
    except Exception as e:
        print("发生错误:", e)

def copy_secure(source_file,destination_file):
    """
    更保险的复制文件
    source_file:源文件路径,例如 "C:/path/to/source.txt"
    destination_file:目标文件路径,例如 "C:/path/to/destination.txt"
    """
    try:
        source_hash = calculate_hash(source_file)

        with open(source_file, 'rb') as src, open(destination_file, 'wb') as dest:
            dest.write(src.read())

        destination_hash = calculate_hash(destination_file)

        if source_hash == destination_hash:
            pass

        else:
            print("文件复制完成，但验证失败：内容不匹配。")

    except FileNotFoundError:
        print("源文件不存在:", source_file)
    except Exception as e:
        print("发生错误:", e)

def copy_secure2(source_file,destination_file):
    """
    更更更保险的复制文件
    source_file:源文件路径,例如 "C:/path/to/source.txt"
    destination_file:目标文件路径,例如 "C:/path/to/destination.txt"
    """

    temp_file = destination_file + '.tmp'

    try:
        shutil.copy2(source_file, temp_file)# 使用copy2

        source_hash = calculate_hash(source_file)

        destination_hash = calculate_hash(temp_file)

        if source_hash == destination_hash:
            os.rename(temp_file, destination_file)

        else:
            print("文件复制完成，但验证失败：内容不匹配。")
            os.remove(temp_file)

    except Exception as e:
        print("发生错误:", e)
        if os.path.exists(temp_file):
            os.remove(temp_file)

def execute_command(command):
    """
    执行给定的命令
    command:命令
    """
    try:
        # 使用 ADB 执行命令
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"命令执行失败: {e}")
        return None

def copy3_secure(source_file,destination_file,yes_or_no = False):
    """
    更更更更保险的方式复制文件
    source_file:源文件路径,例如 "C:/path/to/source.txt"
    destination_file:目标文件路径,例如 "C:/path/to/destination.txt"
    yes_or_no:是否覆盖文件,默认不覆盖.False:不覆盖,True:覆盖
    """
    if os.path.exists(destination_file):
        if yes_or_no != False:
            return

    source_hash = calculate_hash(source_file)
    temp_file = destination_file + '.tmp'

    try:
        chunk_size=4096
        with open(temp_file, 'rb') as source_file:
            with open(destination_file, 'wb') as dest_file:
                while True:
                    chunk = source_file.read(chunk_size)
                    if not chunk:
                        break
                    dest_file.write(chunk)

        temp_hash = calculate_hash(temp_file)

        if source_hash == temp_hash:
                os.rename(temp_file, destination_file)
        else:
            print("文件复制完成，但验证失败：内容不匹配。")
            os.remove(temp_file)

    except FileNotFoundError:
        print("源文件不存在:", source_file)
    except Exception as e:
        print("发生错误:", str(e))
        if os.path.exists(temp_file):
            os.remove(temp_file)

import winreg

def software():
    """获取当前安装的软件列表"""
    software_list = []

    # Windows 64-bit 和 32-bit 注册表路径
    registry_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for registry_key in registry_keys:
        try:
            # 打开注册表项
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        # 读取每个子键的 DisplayName
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            software_list.append(display_name)
                    except FileNotFoundError:
                        continue
        except FileNotFoundError:
            continue

    return software_list

# 获取已安装的软件并打印
installed_software = software()
print("已安装的软件:")
for softwares in installed_software:
    pass

class adb:
    """
    执行ADB命令需要用USB链接安卓设备!!!
    如果没有链接安卓设备ADB命令是无效的!!!
    设备需要 Root 权限：此方法仅在设备已经获得 Root 权限的情况下有效。如果没有 Root 权限，将无法成功切换到 Root 用户。

    安全性：Root 权限将使用户能访问系统的所有文件和资源，这既带来了灵活性，也会提高安全风险。因此要谨慎使用。

    ADB 设置：确保 ADB 已正确安装并与设备成功连接。USB 调试需开启。

    使用风险：使用 Root 权限时需要小心操作，尽量避免侵入系统关键文件或应用，这可能导致系统崩溃或其他技术问题。

    链接安卓设备示例:

    #通过USB链接
    connect_via_usb()
        
    # 获取设备 IP 地址
    device_ip = get_device_ip()
    if device_ip:
        # 通过 Wi-Fi 连接
        connect_via_wifi(device_ip)
        #尝试切换到root用户(Android最高权限,需要Android已解锁root)
        root()
    """

    def install_apk(apk_path):
        """
        安装指定的 APK 文件
        apk_path:apk文件的路径
        """
        try:
            # 使用 ADB 安装 APK 文件
            subprocess.run(["adb", "install", apk_path], check=True)
            print(f"成功安装 APK: {apk_path}")
        except subprocess.CalledProcessError as e:
            print(f"安装失败: {e}")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def uninstall_app(package_name):
        """
        卸载指定包名的应用
        package_name:应用名称
        """
        try:
            # 使用 ADB 卸载应用
            subprocess.run(["adb", "uninstall", package_name], check=True)
            print(f"成功卸载应用: {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"卸载失败: {e}")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def shutdown_device():
        """通过 ADB 命令关闭 Android 设备"""
        try:
            # 使用 ADB 进行关机
            subprocess.run(["adb", "shell", "reboot", "-p"], check=True)
            print("设备正在关机...")
        except subprocess.CalledProcessError as e:
            print(f"关机失败: {e}")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def reboot_device():
        """通过 ADB 命令重启 Android 设备"""
        try:
            # 使用 ADB 进行关机
            subprocess.run(["adb", "reboot"], check=True)
            print("设备正在关机...")
        except subprocess.CalledProcessError as e:
            print(f"关机失败: {e}")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def reboot_to_recovery():
        """通过 ADB 命令重启 Android 设备到恢复模式"""
        try:
            # 使用 ADB 进入恢复模式
            subprocess.run(["adb", "reboot", "recovery"], check=True)
            print("设备正在重启到恢复模式...")
        except subprocess.CalledProcessError as e:
            print(f"重启到恢复模式失败: {e}")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def connect_via_usb():
        """通过 USB 连接 Android 设备"""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)

            if "device" in result.stdout:
                """设备已通过 USB 连接"""
                pass

            else:
                print("没有找到已连接的设备，请确认 USB 调试已开启。")
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")

    def get_device_ip():
        """获取设备的 IP 地址"""
        try:
            result = subprocess.run(["adb", "shell", "ip", "route"], capture_output=True, text=True)
            # 使用正则表达式提取 IP 地址
            ip_address = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
            if ip_address:
                return ip_address.group(0)
            else:
                print("未能获取设备 IP 地址，请确认设备已连接。")
                return None
        except FileNotFoundError:
            print("未找到 ADB，确保 ADB 已安装并正确配置在 PATH 中。")
            return None

    def connect_via_wifi(ip_address):
        """
        通过 Wi-Fi 连接 Android 设备
        ip_address:Android设备的ip地址,可以从get_device_ip函数获取.
        """
        try:
            """进入无限调试模式"""
            subprocess.run(["adb", "tcpip", "5555"], check=True)
            # 通过 IP 地址连接设备
            subprocess.run(["adb", "connect", ip_address + ":5555"], check=True)
            print(f"成功连接到设备：{ip_address}")
        except subprocess.CalledProcessError as e:
            print(f"连接失败: {e}")

    def execute_command(command):
        """
        执行给定的命令
        command:命令
        """
        try:
            # 使用 ADB 执行命令
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"命令执行失败: {e}")
            return None

    def root():
        """尝试切换到 Root 用户"""
        command = ["adb", "shell", "su"]
        output = execute_command(command)

        if "permission denied" in output.lower():
            print("没有权限切换到 Root 用户，确保设备已 Root 并安装了适当的权限管理。")

        else:
            print("已成功切换到 Root 用户。")

def admin():
    """判断有没有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def UAC_admin():
    """弹出请求管理员权限界面"""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

android = main.ADB
folder_path = os.path.expanduser("~")

if __name__ == '__main__':
    print('软件安装列表:',main.softwares)