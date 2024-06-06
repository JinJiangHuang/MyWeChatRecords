from flet import *


class PromptDialog(AlertDialog):
    def __init__(self):
        super().__init__()
        self.bgcolor = colors.WHITE
        self.actions_padding = 5
        self.content_padding = padding.symmetric(5, 30)
        self.title_padding = padding.symmetric(15, 15)
        self.shape = RoundedRectangleBorder(radius=8)
        self.actions = [
            TextButton(content=Text("关闭", size=14), on_click=lambda e: {self.dismiss()})
        ]

    def show(self, page: Page, content):
        self.title = Text(content, size=16, expand=1)
        page.dialog = self
        self.open = True
        page.update()

    def dismiss(self):
        self.open = False
        self.page.update()

