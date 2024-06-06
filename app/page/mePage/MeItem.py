from flet_core import *

from app.person import Me


# 聊天记录列表item
class MeItem(Container):
    def __init__(self):
        super().__init__()
        me = Me()
        self.avatar = CircleAvatar(width=30, height=30, bgcolor=colors.GREY_200,
                                   foreground_image_url=me.smallHeadImgUrl)
        self.user_name = Text(size=14, color=colors.BLACK, value="我的")

        self.user_layout = Row(
            [
                self.avatar,
                Column([self.user_name], spacing=0),
                Container(expand=1),
            ],
        )
        self.padding = padding.symmetric(vertical=5, horizontal=10)
        self.content = self.user_layout

