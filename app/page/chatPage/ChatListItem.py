import flet as ft
from flet_core import *

from app.person import Contact


# 聊天记录列表item
class ChatListItem(Container):
    def __init__(self, contact: Contact = None, on_click=None, is_check=False):
        super().__init__()
        self.height = 60
        if on_click:
            self.on_click = lambda e: on_click(contact)
        # print(contact.remark, contact.smallHeadImgUrl)
        image_path = contact.smallHeadImgUrl
        if len(image_path) == 0 or not image_path:
            image_path = "1234"

        self.avatar = Image(width=30, height=30, src=image_path,
                            error_content=Container(width=30, height=30, bgcolor=colors.GREY_300),
                            border_radius=ft.border_radius.all(5))

        self.user_name = Text(size=13, color="#102057", value=contact.remark, tooltip=contact.remark)
        self.message = Text(size=11, color="#999999", value=contact.nickName, tooltip=contact.nickName)
        self.indicator = Container(width=3, height=0, bgcolor=colors.BLUE)
        self.user_layout = Row(
            [
                self.avatar,
                Column([Container(height=6), self.user_name, self.message],
                       spacing=0),
                Container(expand=1),
                self.indicator
            ],
        )
        self.contact = contact
        self.padding = padding.symmetric(vertical=5, horizontal=10)
        self.content = self.user_layout
        self.set_checked(is_check)

    def set_checked(self, is_check):
        self.bgcolor = colors.GREY_200 if is_check else colors.TRANSPARENT

