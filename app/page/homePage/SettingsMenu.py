from flet_core import *

from app.components.LocalImage import HomeNailLocalImage, MenuLocalImage
from app.config import UrlConfigs


class SettingsMenu(MenuBar):
    def __init__(self):
        super().__init__()
        self.style = MenuStyle(
            padding=0,
            elevation=0,
            bgcolor=colors.TRANSPARENT,
            side=BorderSide(width=0, color=colors.TRANSPARENT),
        )
        text_color = "#666666"
        self.controls = [
            SubmenuButton(
                content=Row([Container(width=4), HomeNailLocalImage("home_nail_settings.png")], spacing=0),
                menu_style=MenuStyle(
                    bgcolor=colors.WHITE,
                    elevation=0,
                    padding=0,
                    side=BorderSide(width=1, color=colors.BLACK26),
                    shadow_color=colors.GREY_200,
                ),
                controls=[
                    MenuItemButton(
                        opacity=0.5,
                        content=Text("文件管理", color=text_color),
                        leading=MenuLocalImage("home_menu_file_manager.png"),
                        # on_click=lambda e: self.on_click_file_manager()
                    ),
                    MenuItemButton(
                        content=Text("帮助", color=text_color),
                        leading=MenuLocalImage("home_menu_help.png"),
                        on_click=lambda e: UrlConfigs.open_url_help()
                    ),
                    MenuItemButton(
                        content=Text("关于", color=text_color),
                        leading=MenuLocalImage("home_menu_about.png"),
                        on_click=lambda e: UrlConfigs.open_url_about()
                    ),
                ]
            )
        ]

    def on_click_file_manager(self):
        pass

