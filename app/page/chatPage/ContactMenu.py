from flet import *

from app.components.LocalImage import MenuLocalImage
from app.page import DataManager
from app.page.RouterManager import Router
from app.person import Contact


class ContactMenu(MenuBar):
    def __init__(self, contact: Contact):
        super().__init__()
        self.style = MenuStyle(
            bgcolor=colors.TRANSPARENT,
            elevation=0,
            padding=0,
            side=BorderSide(width=0, color=colors.TRANSPARENT),
        )
        self.controls = [
            SubmenuButton(
                width=35,
                leading=Icon(icons.MORE_HORIZ, size=20, color=colors.BLACK87),
                menu_style=MenuStyle(
                    bgcolor=colors.WHITE,
                    elevation=0,
                    padding=0,
                    side=BorderSide(width=1, color=colors.BLACK26),
                    shadow_color=colors.GREY_200,
                ),
                controls=[
                    MenuItemButton(
                        content=Text("详情"),
                        leading=MenuLocalImage("chat_menu_detail.png"),
                        on_click=lambda e: {
                            Router().pubsub_show_contact(contact)
                        }
                    ),
                    MenuItemButton(
                        content=Text("统计信息"),
                        leading=MenuLocalImage("chat_menu_stat.png"),
                        on_click=lambda e: DataManager.stat_analysis(contact)
                    ),
                    MenuItemButton(
                        content=Text("年度报告"),
                        leading=MenuLocalImage("chat_menu_year_report.png"),
                        on_click=lambda e: DataManager.year_report(contact)
                    ),
                    MenuItemButton(
                        content=Text("AI情感分析  "),
                        opacity=0.5,
                        leading=MenuLocalImage("chat_menu_motion.png"),
                        # on_click=lambda e: {}
                    ),
                ]
            ),
            SubmenuButton(width=7)
        ]


    # def get_menu_entry(self, contact: Contact) -> Control:
    #     return CupertinoContextMenu(
    #         enable_haptic_feedback=True,
    #         content=Icon(icons.MORE_HORIZ, size=20, color=colors.BLACK87),
    #         actions=[
    #             CupertinoContextMenuAction(
    #                 text="详情",
    #                 trailing_icon=icons.DETAILS,
    #                 on_click=lambda e: {}
    #             ),
    #             CupertinoContextMenuAction(
    #                 text="统计信息",
    #                 trailing_icon=icons.INFO,
    #                 on_click=lambda e: DataManager.stat_analysis(contact)
    #             ),
    #             CupertinoContextMenuAction(
    #                 text="年度报告",
    #                 trailing_icon=icons.REPORT,
    #                 on_click=lambda e: DataManager.year_report(contact)
    #             ),
    #             CupertinoContextMenuAction(
    #                 text="AI情感分析",
    #                 trailing_icon=icons.MOTION_PHOTOS_OFF,
    #                 on_click=lambda e: {}
    #             ),
    #         ]
    #     )