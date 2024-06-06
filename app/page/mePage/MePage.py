from typing import Optional

from flet_core import *

from app.components.ChipContainer import ChipContainer
from app.components.LoadingDialog import LoadingDialog
from app.components.PromptDialog import PromptDialog
from app.page import DataManager
from app.page.RouterManager import Router
from app.page.mePage.MeInfo import MeInfo
from app.page.mePage.MeItem import MeItem
from app.util.exporter.output import Output


# 聊天界面，包含聊天记录列表和聊天详情窗口
class MePage(Row):
    """
        @Author  : youngwm
        @Time    : 2024/5/6
        @IDE     : Pycharm
        @Version : Python3.10
        @comment : ···
        """
    def __init__(self):
        super().__init__()
        self.spacing = 0
        self.expand = True
        #
        self.me_listview: Optional[ListView] = None
        self.user_avatar = None
        self.user_name = None
        self.user_layout = None
        self.layout_me_list = None
        self.layout_me_detail: Optional[Container] = None

        self.init_me_list()
        self.init_me_detail()

        divider = VerticalDivider(color=colors.BLACK12, width=0.7)
        self.controls.clear()
        self.controls.append(self.layout_me_list)
        self.controls.append(divider)
        self.controls.append(self.layout_me_detail)

    def did_mount(self):
        self.setup_me_list()

    def setup_me_list(self):
        self.me_listview.controls.clear()
        # 我的
        self.me_listview.controls.append(MeItem())
        # 操作功能更
        export_chat_history = ChipContainer("me_menu_export_chats.png", content="导出聊天记录(全部)",
                                            on_click=lambda e: {
                                                Router().pubsub_export_chat_history(None)
                                            })
        open_dir_export_chat_history = ChipContainer("me_menu_view_export_chats.png", content="查看导出的聊天记录",
                                                     on_click=lambda e: DataManager.open_msg_history_export_dir())
        export_contact = ChipContainer("me_menu_export_contacts.png", content="导出联系人",
                                       on_click=lambda e: {self.export_data()})
        open_dir_export_contacts = ChipContainer("me_menu_view_export_contacts.png", content="查看导出的联系人",
                                                 on_click=lambda e: DataManager.open_contacts_export_dir())
        export_friend_moment_me = ChipContainer("me_menu_export_friend_activity2.png", content="导出自己朋友圈", opacity=0.5)
        export_friend_moment = ChipContainer("me_menu_export_friend_activity1.png", content="导出朋友圈", opacity=0.5)
        export_collection = ChipContainer("me_menu_export_collect.png", content="导出收藏", opacity=0.5)
        self.me_listview.controls.append(export_chat_history)
        self.me_listview.controls.append(open_dir_export_chat_history)
        self.me_listview.controls.append(export_contact)
        self.me_listview.controls.append(open_dir_export_contacts)
        self.me_listview.controls.append(export_friend_moment_me)
        self.me_listview.controls.append(export_friend_moment)
        self.me_listview.controls.append(export_collection)

        self.layout_me_detail.content = MeInfo()
        self.update()

    def init_me_list(self):
        # 03-01 标题
        self.me_listview = ListView(expand=True, spacing=10)

        # 03- 操作栏
        self.layout_me_list = Container(
            content=Column(
                controls=[
                    # Container(self.user_layout, padding=padding.symmetric(horizontal=15, vertical=10)),
                    Container(self.me_listview, padding=padding.symmetric(0, 20)),
                ],
            ),
            bgcolor=colors.WHITE,
            padding=padding.only(0, 0, 0, 0),
            margin=margin.Margin(0, 0, 0, 0),
            border_radius=0,
            width=230,
        )

    def handle_search_change(self):
        pass

    def handle_search_focus_change(self):
        pass

    def init_me_detail(self):
        self.layout_me_detail = Container(expand=True, padding=0)

    def export_data(self):
        loading = LoadingDialog()

        loading.show(self.page, f"数据导出中..")
        worker = Output(None, type_=Output.CONTACT_CSV,
                        on_export_finish=lambda: {
                            loading.dismiss(),
                            PromptDialog().show(self.page, "导出完成")
                        }
                        )
