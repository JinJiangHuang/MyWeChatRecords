import json
import os.path
import threading
from typing import Optional

from flet_core import *

from app.components.CustomButton import BigButton
from app.config import GlobalConfigs


class LoadingBtn(UserControl):
    def __init__(self, content, loading_prompt, width, on_click, on_loading_finish,
                 on_get_max_task, on_task_finish, on_task_error, on_all_task_success):
        super().__init__()
        self.loading_btn: Optional[BigButton] = None
        self.content = content
        self.loadingContent = loading_prompt
        self.width = width
        self.on_click = on_click
        self.running = False
        self.callback = on_loading_finish
        #
        self.db_path = ""
        self.key = ""
        self.on_get_max_task = on_get_max_task
        self.on_task_finish = on_task_finish
        self.on_task_error = on_task_error
        self.on_all_task_success = on_all_task_success

    def did_mount(self):
        pass

    def will_unmount(self):
        self.running = False

    def build(self):
        self.loading_btn = BigButton(on_click=lambda e: self.on_click(None))
        self.loading_btn.set_text(self.content)
        return self.loading_btn

    def start_thread(self):
        print("开始异步处理")
        if self.running:
            return
        self.running = True
        if self.page.platform == PagePlatform.WINDOWS:
            self.th = threading.Thread(target=self.loading_wx_config_windows, args=(), daemon=True)
            self.th.start()

    def loading_wx_config_windows(self):
        from app.decrypt.get_wx_info import load_wx_config
        import pythoncom  # 仅windows系统支持本库，在mac中找不到，所以放到函数中导入，这样在mac才能运行
        pythoncom.CoInitialize()
        self.loading_btn.set_text(f"{self.loadingContent}")
        result = load_wx_config()
        print("加载/更新聊天记录", result)
        if len(result) > 0:
            self.save_user_info(result[0])
        self.running = False
        self.callback(result)
        self.loading_btn.set_text(f"{self.content}")
        if len(result) > 0:
            config = result[0]
            self.key = config["key"]
            self.db_path = os.path.join(config["filePath"], "Msg")
            if os.path.exists(self.db_path) and len(self.key) > 0:
                self.export_wx_db_windows()
                pass

    def start_process(self):
        if not self.running:
            self.start_thread()

    def save_user_info(self, result):
        # print("Exit clicked")
        dic = {
            'name': result['name'],
            'wxid': result['wxid'],
            'account': result['account'],
            'mobile': result['mobile'],
            'mail': result['mail'],
            'wx_dir': result['filePath'],
            'token': ""
        }
        json_file_path = GlobalConfigs().path_user_info_file
        try:
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(dic, f, ensure_ascii=False, indent=4)
        except:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(dic))

    def export_wx_db_windows(self):
        from app.DataBase import close_db
        from app.DataBase.merge import merge_databases, merge_MediaMSG_databases

        from app.decrypt import decrypt
        close_db()
        path_database_dir = GlobalConfigs().path_database_dir

        os.makedirs(path_database_dir, exist_ok=True)
        tasks = []
        if os.path.exists(self.db_path):
            for root, dirs, files in os.walk(self.db_path):
                for file in files:
                    inpath = os.path.join(root, file)
                    # print("inpath-123", inpath)
                    if '.db' == file[-3:]:
                        if 'xInfo.db' == file:
                            continue
                        output_path = os.path.join(path_database_dir, file)
                        tasks.append([self.key, inpath, output_path])
                    else:
                        try:
                            name, suffix = file.split('.')
                            if suffix.startswith('db_SQLITE'):
                                output_path = os.path.join(path_database_dir, name + '.db')
                                tasks.append([self.key, inpath, output_path])
                        except Exception as e:
                            print("发生异常", inpath, "\n              ", str(e))
                            continue
        self.on_get_max_task(len(tasks))
        print(tasks)
        for i, task in enumerate(tasks):
            if decrypt.decrypt(*task) == -1:
                self.on_task_error(i)
            self.on_task_finish(i)
        # print(self.db_path)
        # 目标数据库文件
        target_database = os.path.join(path_database_dir, 'MSG.db')
        # print("target_database", target_database)
        # 源数据库文件列表
        source_databases = [os.path.join(path_database_dir, f"MSG{i}.db") for i in range(1, 50)]
        # print("源数据库文件列表\n", source_databases)
        import shutil
        if os.path.exists(target_database):
            os.remove(target_database)
        shutil.copy2(os.path.join(path_database_dir, 'MSG0.db'), target_database)  # 使用一个数据库文件作为模板
        # 合并数据库
        merge_databases(source_databases, target_database)

        # 音频数据库文件
        target_database = os.path.join(path_database_dir, 'MediaMSG.db')
        # 源数据库文件列表
        if os.path.exists(target_database):
            os.remove(target_database)
        source_databases = [os.path.join(path_database_dir, f"MediaMSG{i}.db") for i in range(1, 50)]
        shutil.copy2(os.path.join(path_database_dir, 'MediaMSG0.db'), target_database)  # 使用一个数据库文件作为模板

        # 合并数据库
        merge_MediaMSG_databases(source_databases, target_database)
        self.on_all_task_success()
