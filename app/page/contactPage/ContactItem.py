from flet import *

from app.person import Contact


# 聊天记录列表item
class ContactItem(Container):
    def __init__(self, contact: Contact, on_click=None):
        super().__init__()
        self.contact = contact
        self.padding = padding.symmetric(vertical=5, horizontal=10)
        self.height = 60
        #
        if on_click:
            self.on_click = lambda e: on_click(contact)
        self.avatar = CircleAvatar(width=30, height=30, bgcolor=colors.GREY_300,
                                   foreground_image_url=self.contact.smallHeadImgUrl)
        self.user_name = Text(self.contact.remark, size=13.5, color="#102057", tooltip=contact.remark)
        self.message = Text(size=11, color="#999999", value=self.contact.nickName, tooltip=contact.nickName)
        self.content = Row(
            [
                self.avatar,
                Column([Container(height=6), self.user_name, self.message],
                       spacing=0),
                Container(expand=1)
            ],
        )

    def set_checked(self, is_check):
        self.bgcolor = colors.GREY_200 if is_check else colors.TRANSPARENT

