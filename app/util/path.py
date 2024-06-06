import getpass
import os
import platform
import sys
import winreg

from app.config import GlobalConfigs
from app.util import image

# os.makedirs('./data/image', exist_ok=True)


def get_abs_path(path, base_path):
    from app.person import Me
    # return os.path.join(os.getcwd(), 'app/data/icons/404.png')
    if path:
        path_source = os.path.join(Me().wx_dir, path)
        # print("微信目录", Me().wx_dir)
        # print("微信内图片", path_source)
        output_path = image.decode_dat(path_source, base_path)
        return output_path if output_path else ':/icons/icons/404.png'
    else:
        return ':/icons/icons/404.png'

pass


def get_desktop_path():
    """
    获取桌面的路径
    :return:
    """
    user_name = getpass.getuser()  # 获取当前用户名
    path = "/users/" + user_name + "/Desktop/"
    if platform.system().lower() == "windows":
        path = "C:\\Users\\" + user_name + "\\Desktop\\"
    return path

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    # PyInstaller会将资源文件打包到一个临时文件夹中，运行时可以通过sys._MEIPASS访问
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_relative_path(path, base_path, type_='image'):
    from app.person import Me
    if path:
        base_path = os.getcwd() + base_path
        output_path = image.decode_dat(os.path.join(Me().wx_dir, path), base_path)
        relative_path = './image/' + os.path.basename(
            output_path) if output_path else 'https://www.bing.com/images/search?view=detailV2&ccid=Zww6woP3&id=CCC91337C740656E800E51247E928ACD3052FECF&thid=OIP.Zww6woP3Em49TdSG_lnggAHaEK&mediaurl=https%3a%2f%2fmeekcitizen.files.wordpress.com%2f2018%2f09%2f404.jpg%3fw%3d656&exph=360&expw=640&q=404&simid=608040792714530493&FORM=IRPRST&ck=151E7337A86F1B9C5C5DB08B15B90809&selectedIndex=21&itb=0'
        return relative_path
    else:
        return ':/icons/icons/404.png'


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def wx_path():
    try:
        is_w_dir = False

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "FileSavePath")
            winreg.CloseKey(key)
            w_dir = value
            is_w_dir = True
        except Exception as e:
            w_dir = "MyDocument:"

        if not is_w_dir:
            try:
                user_profile = os.environ.get("USERPROFILE")
                path_3ebffe94 = os.path.join(user_profile, "AppData", "Roaming", "Tencent", "WeChat", "All Users",
                                             "config",
                                             "3ebffe94.ini")
                with open(path_3ebffe94, "r", encoding="utf-8") as f:
                    w_dir = f.read()
                is_w_dir = True
            except Exception as e:
                w_dir = "MyDocument:"

        if w_dir == "MyDocument:":
            try:
                # 打开注册表路径
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
                documents_path = winreg.QueryValueEx(key, "Personal")[0]  # 读取文档实际目录路径
                winreg.CloseKey(key)  # 关闭注册表
                documents_paths = os.path.split(documents_path)
                if "%" in documents_paths[0]:
                    w_dir = os.environ.get(documents_paths[0].replace("%", ""))
                    w_dir = os.path.join(w_dir, os.path.join(*documents_paths[1:]))
                    # print(1, w_dir)
                else:
                    w_dir = documents_path
            except Exception as e:
                profile = os.environ.get("USERPROFILE")
                w_dir = os.path.join(profile, "Documents")
        msg_dir = os.path.join(w_dir, "WeChat Files")
        return msg_dir
    except FileNotFoundError:
        return '.'
