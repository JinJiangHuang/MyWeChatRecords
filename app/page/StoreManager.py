"""
    管理本地存储
    @Author  : youngwm
    @Time    : 2024/5/6
    @IDE     : Pycharm
    @Version : Python3.10
    @comment : ···
"""

from flet_core import *

from app.person import Contact


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class StoreGlobalManager:

    def __init__(self):
        self.page = None
        self.client_storage = None

    def init(self, page: Page):
        self.page = page
        self.client_storage = page.client_storage


class HomeStorageManager:
    key_home_page_index = "key_home_page_index"

    @staticmethod
    def save_homepage_index(index):
        StoreGlobalManager().client_storage.set(key=HomeStorageManager.key_home_page_index, value=index)

    @staticmethod
    def get_homepage_index():
        return StoreGlobalManager().client_storage.get(key=HomeStorageManager.key_home_page_index)

    key_current_wx_save_dir_name = "key_current_wx_save_dir_name"

    @staticmethod
    def save_wx_save_dir(value):
        StoreGlobalManager().client_storage.set(key=HomeStorageManager.key_current_wx_save_dir_name, value=value)

    @staticmethod
    def get_wx_save_dir():
        return StoreGlobalManager().client_storage.get(key=HomeStorageManager.key_current_wx_save_dir_name)


class ChatStorageManager:
    """
    本地数据缓存
    """
    key_chat_page_index = "key_chat_page_index"
    key_chat_page_contact = "key_chat_page_contact"

    @staticmethod
    def save_chat_page_index(index):
        if StoreGlobalManager().client_storage:
            StoreGlobalManager().client_storage.set(key=ChatStorageManager.key_chat_page_index, value=index)

    @staticmethod
    def get_chat_page_index():
        if StoreGlobalManager().client_storage:
            return StoreGlobalManager().client_storage.get(key=ChatStorageManager.key_chat_page_index)

    @staticmethod
    def save_chat_page_contact(contact: Contact):
        if StoreGlobalManager().client_storage:
            data = str(contact)
            StoreGlobalManager().client_storage.set(key=ChatStorageManager.key_chat_page_contact, value=data)

    @staticmethod
    def get_chat_page_contact():
        if StoreGlobalManager().client_storage:
            data = StoreGlobalManager().client_storage.get(key=ChatStorageManager.key_chat_page_contact)
            return data


class ContactStorageManager:
    key_contact_page_index = "key_contact_page_index"

    @staticmethod
    def save_contact_page_index(index):
        StoreGlobalManager().client_storage.set(key=ContactStorageManager.key_contact_page_index, value=index)

    @staticmethod
    def get_contact_page_index():
        return StoreGlobalManager().client_storage.get(key=ContactStorageManager.key_contact_page_index)


class ExportStorageManager:
    key_export_page_index = "key_export_page_index"

    @staticmethod
    def save_contact_page_index(index):
        StoreGlobalManager().client_storage.set(key=ExportStorageManager.key_export_page_index, value=index)

    @staticmethod
    def get_contact_page_index():
        return  StoreGlobalManager().client_storage.get(key=ExportStorageManager.key_export_page_index)