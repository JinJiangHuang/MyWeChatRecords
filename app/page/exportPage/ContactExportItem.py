from flet import *

from app.person import Contact


# 聊天记录列表item
class ContactExportItem(Container):
    def __init__(self, contact: Contact, on_check_change):
        super().__init__()
        self.contact = contact
        self.height = 50
        self.on_check_change = on_check_change
        self.padding = padding.symmetric(vertical=5, horizontal=0)
        #
        self.check_box = Checkbox(
            active_color="#0046ff",
            height=14, width=14,
            shape=CircleBorder(),
            border_side=BorderSide(width=0.5, color="#999999"),
            on_change=lambda e: self.notify_check_change())

        self.avatar = CircleAvatar(width=30, height=30, bgcolor=colors.GREY_300,
                                   foreground_image_url=self.contact.smallHeadImgUrl)
        self.user_name = Text(self.contact.remark, size=13, color="#102057",
                              tooltip=contact.remark)
        self.message = Text(size=12, color="#999999", value=self.contact.nickName, tooltip=contact.nickName)
        self.content = Row(
            [
                Container(width=8),
                self.check_box,
                Row(
                    [
                        self.avatar,
                        Column(
                            [
                                Container(height=10),
                                self.user_name,
                            ],
                            spacing=0),
                    ],
                )
            ], spacing=10
        )
        self.on_click = lambda e: (self.toggle_checkbox())

    def toggle_checkbox(self):
        self.check_box.value = not self.check_box.value
        self.notify_check_change()
        self.update()

    def notify_check_change(self):
        is_check = self.check_box.value
        self.on_check_change(is_check)
        self.bgcolor = colors.GREY_200 if is_check else colors.TRANSPARENT

    def set_checked(self, is_check):
        self.check_box.value = is_check
        self.notify_check_change()
