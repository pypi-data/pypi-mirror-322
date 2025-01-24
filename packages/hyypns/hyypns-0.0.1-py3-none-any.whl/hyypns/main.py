from . import __main__
import os

"""Here are some settings."""

adb = __main__.adb

ADB = adb
folder_path = os.path.expanduser("~")
HYY = "hyy","Thank you for using my module."
DESKTOP = __main__.desktop()
USERNAME = __main__.username()

installed_software = __main__.software()

for softwares in installed_software:
    """softwares:当前安装的软件."""
    pass