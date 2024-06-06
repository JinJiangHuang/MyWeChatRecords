from flet import *


class LoadingDialog(AlertDialog):
    def __init__(self):
        super().__init__()
        # self.modal = True
        self.bgcolor = colors.WHITE
        self.content = CupertinoActivityIndicator(
            radius=20,
            color=colors.RED,
            animating=True
        )

    def show(self, page: Page, content="加载中..."):
        self.title = Text(content, size=18, expand=1)
        page.dialog = self
        self.open = True
        page.update()

    def dismiss(self):
        self.open = False
        self.page.update()

