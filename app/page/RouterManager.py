"""
    页面路由跳转
    @Author  : youngwm
    @Time    : 2024/5/6
    @IDE     : Pycharm
    @Version : Python3.10
    @comment : ···
    """
from typing import Optional

from flet_core import *

from app.person import Contact

path_root = ""
path_login = "/login"
path_register = "/register"
path_load_data_page = "/load_wechat_data_page"
path_reset_password = "/reset_password"

topic_export_chat_history = "topic_export_chat_history"
topic_show_chat = "topic_show_chat"
topic_show_contact = "topic_show_contact"


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class Router:
    def __init__(self):
        self.page: Optional[Page] = None
        super().__init__()

    def set_page(self, page: Page):
        self.page = page

    def go(self, path_router: str):
        page = self.page
        if page:
            page.go(path_router)
            page.update()

    def go_home_page(self):
        self.go(path_root)

    def go_load_page(self):
        self.go(path_load_data_page)

    def go_login_page(self):
        self.go(path_login)

    def go_register_page(self):
        self.go(path_register)

    def go_reset_password_page(self):
        self.go(path_reset_password)

    def pubsub_send_topic(self, topic, message):
        page = self.page
        if page:
            page.pubsub.send_all_on_topic(topic, message)

    def pubsub_export_chat_history(self, contact: Optional[Contact] = None):
        self.pubsub_send_topic(topic_export_chat_history, contact)

    def pubsub_show_chat(self, contact: Optional):
        self.pubsub_send_topic(topic_show_chat, contact)

    def pubsub_show_contact(self, contact: Optional):
        self.pubsub_send_topic(topic_show_contact, contact)
