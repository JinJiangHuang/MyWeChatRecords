from flet import *

from app.config import UrlConfigs


class ItemText(Row):
    def __init__(self, value: str, spans=None):
        super().__init__()
        if spans is None:
            spans = []
        self.controls = [
            Container(width=6, height=6, bgcolor="#0046FF"),
            Text(color="#aa333333", size=14, value=value, weight=FontWeight.BOLD, spans=spans)
        ]


class ItemTextList(Column):
    def __init__(self):
        super().__init__()
        self.controls = [
            ItemText("本电脑登录微信PC版本;"),
            ItemText(r"在手机上将聊天记录“迁移到电脑”;  ", spans=[
                TextSpan("查看详情",
                         style=TextStyle(
                             color="#0046FF",
                             decoration_color="#0046FF",
                             decoration=TextDecoration.UNDERLINE),
                         on_click=lambda e: self.on_click_detail())
            ]),
            ItemText(r"迁移后，重新登录微信;"),
        ]

    def on_click_detail(self):
        UrlConfigs.open_url_help()
