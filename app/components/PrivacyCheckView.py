from flet import *

from app.config import UrlConfigs


class PrivacyCheckView(Column):
    def __init__(
            self,
            check=False,
            on_check_change=None,
            on_click_privacy=None,
            on_click_service=None,
            on_click_github_url=None,
    ):
        super().__init__()
        self.spacing = 0
        self.on_check_change = on_check_change
        #
        self.checkbox = CupertinoCheckbox(value=check, on_change=lambda event: self.on_check_change(event.data))
        text_size = 14
        text_color1 = colors.BLACK
        text_color2 = colors.BLUE_300
        text1 = Container(
            Text("我已阅读并同意", size=text_size, color=text_color1),
            on_click=lambda e: self.on_click_text1()
        )
        text2 = Container(
            Text("《隐私协议》", size=text_size, color=text_color2),
            on_click=on_click_privacy
        )
        text3 = Text(" 和 ", size=text_size, color=text_color1)
        text4 = Container(
            Text("《用户协议》", size=text_size, color=text_color2),
            on_click=on_click_service
        )
        row_check = Row(
            controls=[self.checkbox, text1, text2, text3, text4],
            spacing=0
        )
        self.controls.append(row_check)
        #
        text_size2 = 14
        text_color3 = colors.BLACK26
        prompt = "蜜蜂AI会读取你本地微信聊天数据，所有数据都在本地电脑处理。\n本应用已开源"
        text_prompt = Text(value=prompt, size=text_size2, color=text_color3,
                           spans=[
                               TextSpan("(在github查看)",
                                        style=TextStyle(size=text_size2, color=text_color3,
                                                        decoration_color=colors.BLACK26,
                                                        decoration=TextDecoration.UNDERLINE),
                                        on_click=lambda e: UrlConfigs.open_url_github_mine()),
                               TextSpan(",使用第三方开源库", style=TextStyle(size=text_size2, color=text_color3)),
                               TextSpan("(在github查看)",
                                        TextStyle(size=text_size2, color=text_color3,
                                                  decoration_color=colors.BLACK26,
                                                  decoration=TextDecoration.UNDERLINE),
                                        on_click=lambda e: UrlConfigs.open_url_github_from()),
                               TextSpan("读取聊天数据", style=TextStyle(size=text_size2, color=text_color3)),
                               TextSpan("\n使用本产品只能用于管理自己微信聊天记录",  style=TextStyle(size=text_size2, color=text_color3), ),
                           ]
                           )
        row_prompt = Row(
            controls=[Container(width=11), text_prompt],
            spacing=0
        )
        self.controls.append(row_prompt)

    def on_click_text1(self):
        is_check = not self.checkbox.value
        self.checkbox.value = is_check
        self.checkbox.update()
        if self.on_check_change:
            self.on_check_change(is_check)
