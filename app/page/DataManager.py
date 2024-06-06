"""
    微信数据相关管理
    @Author  : youngwm
    @Time    : 2024/5/6
    @IDE     : Pycharm
    @Version : Python3.10
    @comment : ···
    """
import os
import threading
import webbrowser
from datetime import datetime
from typing import Optional

from flet_core import *

from app.DataBase import msg_db
from app.components.PreActionDialog import LoginWechatAlertDialog
from app.config import GlobalConfigs
from app.decrypt.get_wx_info import load_wx_config, error_wechat_no_run
from app.page.StoreManager import HomeStorageManager
from app.person import Contact, Me
from app.util.DirUtils import dirUtils

_port = '21314'


def stat_analysis(contact: Contact):
    """
    统计分析
    """

    def start_web_server():
        from app.web_ui import web
        web.contact = contact
        web.time_range = None
        web.run(port=_port)

    th = threading.Thread(target=start_web_server, args=(), daemon=True)
    th.start()
    webbrowser.open(f"http://127.0.0.1:{21314}/charts/{contact.wxid}")


def year_report(contact: Contact):
    """
    圣诞节年度报告
    """

    def start_web_server():
        from app.web_ui import web
        web.time_range = date_range
        web.contact = contact
        web.time_range = None
        web.run(port=_port)

    date_range = None
    chat_calendar = msg_db.get_messages_calendar(contact.wxid)
    if chat_calendar:
        start_time = datetime.strptime(chat_calendar[0], "%Y-%m-%d")
        end_time = datetime.strptime(chat_calendar[-1], "%Y-%m-%d")
        date_range = (start_time.date(), end_time.date())
    th = threading.Thread(target=start_web_server, args=(), daemon=True)
    th.start()
    webbrowser.open(f"http://127.0.0.1:{21314}/christmas/{contact.wxid}")


def get_msg_avatar_path(is_send, message: dict, contact: Contact, is_absolute_path=True) -> str:
    if is_absolute_path:
        if contact.is_chatroom:
            avatar = message[13].smallHeadImgUrl
        else:
            avatar = Me().smallHeadImgUrl if is_send else contact.smallHeadImgUrl
    else:
        if contact.is_chatroom:
            avatar = message[13].smallHeadImgUrl
        else:
            avatar = Me().smallHeadImgUrl if is_send else contact.smallHeadImgUrl
    return avatar


def open_msg_history_export_dir(contact: Optional[Contact] = None):
    config = GlobalConfigs()
    dir_path = config.path_export_dir
    if contact:
        dir_path = os.path.join(config.path_export_dir, contact.get_uniquid_name())
    os.makedirs(dir_path, exist_ok=True)
    dirUtils.open_dir(dir_path)
    pass


def open_contacts_export_dir():
    dir_path = GlobalConfigs().path_contacts_dir
    os.makedirs(dir_path, exist_ok=True)
    dirUtils.open_dir(dir_path)
    pass


def update_configs(result=None):
    if not result:
        result = load_wx_config()
    if result and len(result) > 0:
        data = result[0]
        if isinstance(data, dict):
            wxid = data.get('wxid')
            name = data.get("name")
            current_usr_wxid = f"【{name}】{wxid}"
            HomeStorageManager().save_wx_save_dir(current_usr_wxid)
            GlobalConfigs().update_user_wxid(current_usr_wxid)


def check_wx_is_login(page: Page):
    result = load_wx_config()
    if result == error_wechat_no_run:
        LoginWechatAlertDialog().show(page)
    else:
         update_configs(result)


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class WxDataManager:
    def __init__(self):
        super().__init__()
        self.contact_list: list[Contact] = []
        self.is_contact_load_finish = False

    def get_contact_list(self) -> list[Contact]:
        if not self.is_contact_load_finish:
            self.contact_list = self.load_contact_list()
        return self.contact_list

    def set_reload_contacts(self):
        self.is_contact_load_finish = False

    def load_contact_list(self) -> list[Contact]:
        """
        加载数据库中联系人列表
        """
        from app.DataBase import micro_msg_db, misc_db, msg_db, close_db, hard_link
        contact_list = []
        micro_msg_db.init_database()
        if not msg_db.open_flag:
            print("load_contact_list 错误", "数据库不存在\n请先解密数据库")
            return contact_list
        print("load_contact_list 数据库加载成功")
        contact_info_lists = micro_msg_db.get_contact()
        # print(contact_info_lists)
        if not contact_info_lists:
            print("WxDataManager 错误", "数据库错误，请重启电脑后重试")
            close_db()
            try:
                pass
                # shutil.rmtree('./app/Database/Msg')
            except:
                pass
            return contact_list

        for i, contact_info_list in enumerate(contact_info_lists):
            # UserName, Alias,Type,Remark,NickName,PYInitial,RemarkPYInitial,ContactHeadImgUrl.smallHeadImgUrl,ContactHeadImgUrl,bigHeadImgUrl
            detail = hard_link.decodeExtraBuf(contact_info_list[9])
            contact_info = {
                'UserName': contact_info_list[0],
                'Alias': contact_info_list[1],
                'Type': contact_info_list[2],
                'Remark': contact_info_list[3],
                'NickName': contact_info_list[4],
                'smallHeadImgUrl': contact_info_list[7],
                'detail': detail,
                'label_name': contact_info_list[10],
            }
            contact = Contact(contact_info)
            contact.smallHeadImgBLOG = misc_db.get_avatar_buffer(contact.wxid)
            contact.set_avatar(contact.smallHeadImgBLOG)
            contact_list.append(contact)
            # print(contact_info)
            pass
        self.is_contact_load_finish = True
        return contact_list
