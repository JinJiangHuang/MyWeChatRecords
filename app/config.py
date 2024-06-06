import getpass
import os
import platform
import sys
import webbrowser


def get_local_assert_path():
    file_path = './app/assets'
    if not os.path.exists(file_path):
        resource_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        file_path = os.path.join(resource_dir, 'app', 'assets')
    return file_path


def get_local_image_path():
    file_path = get_local_assert_path()
    return os.path.join(file_path, 'image')


def get_local_image_file_path(file_name) -> str:
    return os.path.join(get_local_image_path(), file_name)


def get_local_font_path():
    file_path = get_local_assert_path()
    return os.path.join(file_path, 'fonts')


def get_local_font_file_path(file_name):
    return os.path.join(get_local_font_path(), file_name)


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class GlobalConfigs:
    def __init__(self):
        self.current_usr_wxid = 'un_login'
        self.path_export_root_dir = os.path.join(self.get_desktop_path(), '微信聊天记录', self.current_usr_wxid)
        # 数据存放文件路径
        self.path_user_data = os.path.join(self.path_export_root_dir, 'user_data')
        self.path_user_info_file = os.path.join(self.path_user_data, 'info.json')  # 个人信息文件
        self.path_database_dir = os.path.join(self.path_export_root_dir, 'database')
        self.path_export_dir = os.path.join(self.path_export_root_dir, '聊天记录')  # 输出文件夹
        self.path_contacts_dir = os.path.join(self.path_export_root_dir, '联系人')  # 导出联系人
        self.path_data_dir = os.path.join(self.path_export_root_dir, 'data')  #
        # 全局参数
        self.SEND_LOG_FLAG = True  # 是否发送错误日志
        self.SERVER_API_URL = ''  # api接口

    def update_user_wxid(self, data):
        # return
        self.current_usr_wxid = data
        self.path_export_root_dir = os.path.join(self.get_desktop_path(), '微信聊天记录', self.current_usr_wxid)
        # 数据存放文件路径
        self.path_user_data = os.path.join(self.path_export_root_dir, 'user_data')
        os.makedirs(self.path_user_data, exist_ok=True)
        self.path_user_info_file = os.path.join(self.path_user_data, 'info.json')  # 个人信息文件
        self.path_database_dir = os.path.join(self.path_export_root_dir, 'database')
        os.makedirs(self.path_database_dir, exist_ok=True)
        self.path_export_dir = os.path.join(self.path_export_root_dir, '聊天记录')  # 输出文件夹
        os.makedirs(self.path_export_dir, exist_ok=True)
        self.path_contacts_dir = os.path.join(self.path_export_root_dir, '联系人')  # 导出联系人
        os.makedirs(self.path_contacts_dir, exist_ok=True)
        self.path_data_dir = os.path.join(self.path_export_root_dir, 'data')
        os.makedirs(self.path_contacts_dir, exist_ok=True)
        print("更新保存目录", self.current_usr_wxid)

    def get_desktop_path(self):
        """
        获取桌面的路径
        :return:
        """
        user_name = getpass.getuser()  # 获取当前用户名
        path = "/users/" + user_name + "/Desktop/"
        if platform.system().lower() == "windows":
            path = "C:\\Users\\" + user_name + "\\Desktop\\"
        return path


class UrlConfigs:
    # 帮助
    URL_HELP = "https://ktkzutzbtj.feishu.cn/wiki/U29nwbCKoiWZ9xk23IZcdJXmnXg"
    # 关于
    URL_ABOUT = "https://ktkzutzbtj.feishu.cn/wiki/Qq2QwbOFWi0rqLkhnEFcMRl5nMc"
    # 项目来源github
    URL_GITHUB_FROM = "https://github.com/LC044/WeChatMsg"
    # 我的代码github
    URL_GITHUB_MINE = "https://github.com/youngWM/MyWeChatRecords"
    # 隐私协议
    URL_PRIVACY = "https://ktkzutzbtj.feishu.cn/wiki/GQXLwdMyDiVdNjkbk40cxPfsnKd"
    # 用户协议
    URL_SERVICE_ITEMS = "https://ktkzutzbtj.feishu.cn/wiki/LoGxw9plYiyWCmkPablcbegmnpe"

    @staticmethod
    def open_url(url):
        webbrowser.open(url)

    @staticmethod
    def open_url_help():
        UrlConfigs.open_url(UrlConfigs.URL_HELP)

    @staticmethod
    def open_url_about():
        UrlConfigs.open_url(UrlConfigs.URL_ABOUT)

    @staticmethod
    def open_url_github_from():
        UrlConfigs.open_url(UrlConfigs.URL_GITHUB_FROM)

    @staticmethod
    def open_url_github_mine():
        UrlConfigs.open_url(UrlConfigs.URL_GITHUB_MINE)

    @staticmethod
    def open_url_privacy():
        UrlConfigs.open_url(UrlConfigs.URL_PRIVACY)

    @staticmethod
    def open_url_service_items():
        UrlConfigs.open_url(UrlConfigs.URL_SERVICE_ITEMS)
