from flet import *

from app.page.RouterManager import Router


class LoginWechatAlertDialog(AlertDialog):
    def __init__(self):
        super().__init__()
        self.modal = True
        self.bgcolor = colors.WHITE
        self.title = Text("安全操作提示", size=18, expand=1)
        self.content = Container(
            Text("1.为保证个人微信数据安全，用户需登录本机微信，确保微信为个人所有！"
                 "\n2.当前微信未登录，请登录后点击刷新按键。",
                 color=colors.BLACK, weight=FontWeight.BOLD),
        )
        self.actions = [
            TextButton("刷新", on_click=lambda e: Router().go_load_page()),
            TextButton("关闭", on_click=lambda e: self.dismiss()),
        ]

    def show(self, page: Page):
        page.dialog = self
        self.open = True
        page.update()

    def dismiss(self):
        self.open = False
        self.page.update()

