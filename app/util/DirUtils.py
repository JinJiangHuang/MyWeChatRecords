import getpass
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from send2trash import send2trash


class dirUtils:

    def __init__(self):
        super(dirUtils, self).__init__()

    @staticmethod
    def open_dir(path_dir):
        """
        打开给定路径的文件夹，在Mac系统级目录下的文件打开失效
        @param path_dir: 打开的目录路径
        @return: 是否打开成功
        """
        if not Path(path_dir).is_dir():
            print(path_dir + "目录不存在！")
            return False
        if platform.system().lower() == "windows":
            os.startfile(path_dir)
            return
        # 无法打开/Users/youngwm/Library/Application Support/Shadowbot/users 下的文件夹
        # 可能是由于路径中包含空格字符而导致的
        # cmd = "open " + path_dir
        cmd = 'open "' + path_dir + '"'
        os.system(cmd)
        print('打开文件夹：' + path_dir)
        return True

    @staticmethod
    def open_and_select_dir(path_dir):
        """
        打开给定路径的文件夹，在Mac系统级目录下的文件打开失效
        @param path_dir: 打开的目录路径
        @return: 是否打开成功
        """
        if not Path(path_dir).is_dir():
            print("open_and_select_dir:", path_dir + "目录不存在！")
            return False

        if platform.system().lower() == "windows":
            os.startfile(path_dir)
        else:
            subprocess.run(['open', '-R', path_dir])
        print('打开并选中文件夹：' + path_dir)
        return True

    @staticmethod
    def delete_dir_forever(dir_path):
        """
        永久删除文件夹
        @param dir_path: 文件夹路径
        @return:
        """
        if not os.path.exists(dir_path):
            return True
        try:
            shutil.rmtree(dir_path)
            if not os.path.exists(dir_path):
                os.removedirs(dir_path)
            print(f"文件夹删除成功！{dir_path}")
            return True
        except OSError as e:
            print(f"文件夹删除失败：{e}")
            return False

    @staticmethod
    def move_to_trash(path):
        """
        移到垃圾桶中
        :param path:
        :return:
        """
        if os.path.exists(path):
            send2trash(path)
            print(f"成功将 {path} 移动到垃圾桶中")
        else:
            print(f"{path} 不存在")

    @staticmethod
    def copy_folder(source_folder, destination_folder):
        """
        复制文件夹内容到新文件夹中
        @param source_folder: 复制来源文件夹
        @param destination_folder: 复制到的文件夹
        @return: boolean 是否复制成功
        """
        if os.path.exists(source_folder) and os.path.isdir(source_folder) and os.path.isdir(destination_folder):
            # 清空原有文件，再执行复制操作，防止增加文件
            if os.path.exists(destination_folder):  # 判断文件夹是否存在
                dirUtils.delete_dir_forever(destination_folder)  # 删除文件夹
            # 备份文件夹
            shutil.copytree(source_folder, destination_folder)
        else:
            print("文件夹不存在！", source_folder)
            return False

    @staticmethod
    def get_sub_dir_name_list(path):
        subdirectories = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                subdirectories.append(item)
        return subdirectories

    # 最近的更新时间对子文件夹进行排序
    @staticmethod
    def get_sub_dir_name_list_by_sort(path, sort_by_time=False):
        subdirectories = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                subdirectories.append((item, os.path.getmtime(item_path)))

        if sort_by_time:
            subdirectories.sort(key=lambda x: x[1], reverse=True)
            subdirectories = [subdir[0] for subdir in subdirectories]
        else:
            subdirectories = [subdir[0] for subdir in subdirectories]

        return subdirectories

    @staticmethod
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

    @staticmethod
    def get_dir_split_flag():
        """
        获取当前系统中目录之间的分隔符
        :return:
        """
        path = "/"
        if platform.system().lower() == "windows":
            path = "\\"
        return path

    @staticmethod
    def get_flet_app_dir_path():
        """
        获取应用包的路径，Python代码打包成应用后，绝对路径获取不到绝对路径。需要专门的方法
        https://blog.csdn.net/qq_31801903/article/details/81666124
        :return:
        """
        # 如果是在 PyInstaller 打包后的应用中
        if getattr(sys, 'frozen', False):
            # 获取打包后应用的临时目录路径
            abs_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        else:
            # 如果是在普通的 Python 环境中
            current_file_path = os.path.abspath(__file__)
            abs_path = os.path.dirname(current_file_path)
        pass
        return abs_path

