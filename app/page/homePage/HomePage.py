from flet_core import *

from app import config
from app.components.LocalImage import HomeNailLocalImage, IconLocalImage
from app.page import RouterManager
from app.page.RouterManager import Router
from app.page.StoreManager import HomeStorageManager
from app.page.chatPage.ChatPage import ChatPage
from app.page.contactPage.ContactPage import ContactPage
from app.page.exportPage.ExportPage import ExportPage
from app.page.homePage.SettingsMenu import SettingsMenu
from app.page.mePage.MePage import MePage


class HomePage(Row):
    def __init__(self):
        super().__init__()
        #
        self.expand = True
        self.spacing = 0
        #
        self.current_nail_index = 0
        if not self.current_nail_index:
            self.current_nail_index = 0

        # ==================================================================
        # 侧边导航栏
        # 头部
        self.avatar = CircleAvatar(bgcolor=colors.WHITE, width=38, height=38,
                                      content=Container(
                                          Image(
                                              src=config.get_local_image_file_path("logo_bee.png")
                                          ),
                                          padding=6, opacity=1
                                      ))
        layout_head = Column([Container(height=15), self.avatar, Container(height=30)])
        # 底部
        import_icon = Container(HomeNailLocalImage("home_nail_load.png"), ink=True,
                                padding=padding.symmetric(5, 0),
                                tooltip="加载/更新聊天记录",
                                on_click=lambda e: Router().go_load_page(), width=60)
        settings_icon = SettingsMenu()
        trailing_layout = Column([Container(height=100), import_icon, settings_icon],
                                 horizontal_alignment=CrossAxisAlignment.CENTER, spacing=0)
        text_size = 11
        self.rail = NavigationRail(
            selected_index=self.current_nail_index,
            bgcolor="#0046ff",
            indicator_color=colors.TRANSPARENT,
            indicator_shape=None,
            label_type=NavigationRailLabelType.ALL,
            leading=layout_head,
            trailing=trailing_layout,
            min_width=40,
            min_extended_width=40,
            destinations=[
                NavigationRailDestination(
                    icon_content=HomeNailLocalImage("home_nail_chat_1.png"),
                    selected_icon_content=HomeNailLocalImage("home_nail_chat_2.png"),
                    label_content=Text("聊天", color=colors.WHITE54, size=text_size),
                    padding=0
                ),
                NavigationRailDestination(
                    icon_content=HomeNailLocalImage("home_nail_contact_1.png"),
                    selected_icon_content=HomeNailLocalImage("home_nail_contact_2.png"),
                    label_content=Text("好友", color=colors.WHITE54, size=text_size),
                    padding=0
                ),
                NavigationRailDestination(
                    icon_content=HomeNailLocalImage("home_nail_manager_1.png"),
                    selected_icon_content=HomeNailLocalImage("home_nail_manager_2.png"),
                    label_content=Text("管理", color=colors.WHITE54, size=text_size),
                    padding=0
                ),
                NavigationRailDestination(
                    icon_content=HomeNailLocalImage("home_nail_export_1.png"),
                    selected_icon_content=HomeNailLocalImage("home_nail_export_2.png"),
                    label_content=Text("导出", color=colors.WHITE54, size=text_size),
                    padding=0,
                ),
            ],
            on_change=lambda e: self.handle_dest_change(e.control.selected_index),
        )

        # ==================================================================
        # 导航目的页面
        self.chat_page = ChatPage()
        self.contact_page = ContactPage()
        self.me_page = MePage()
        self.export_page = ExportPage()
        self.is_need_init_nail_dest_page = False  # 是否需要初始化导航目的地页面
        #
        self.dest_layout = Column(alignment=MainAxisAlignment.START, expand=True, spacing=0)
        self.controls = [
            WindowDragArea(self.rail),
            VerticalDivider(width=1),
            self.dest_layout,
        ]

    def did_mount(self):
        page = self.page
        page.title = "蜜蜂AI聊天记录管理"
        page.window_width = 900
        page.window_height = 600
        page.window_min_width = page.window_width
        page.window_min_height = page.window_height
        page.window_bgcolor = colors.GREY_100
        self.handle_dest_change(0)
        page.pubsub.subscribe_topic(RouterManager.topic_export_chat_history, self.on_receive_export_event)
        page.pubsub.subscribe_topic(RouterManager.topic_show_chat, self.on_receive_export_event)
        page.pubsub.subscribe_topic(RouterManager.topic_show_contact, self.on_receive_export_event)
        page.window_title_bar_hidden = True
        page.update()

    def will_unmount(self):
        self.page.pubsub.unsubscribe_topic(RouterManager.topic_export_chat_history)
        self.page.pubsub.unsubscribe_topic(RouterManager.topic_show_chat)
        self.page.pubsub.unsubscribe_topic(RouterManager.topic_show_contact)

    def on_receive_export_event(self, topic, contact):
        if topic == RouterManager.topic_export_chat_history:
            self.handle_dest_change(3)
            self.export_page.on_receive_export_event(topic=topic, contact=contact)
        elif topic == RouterManager.topic_show_chat:
            self.handle_dest_change(0)
            self.chat_page.on_receive_show_event(topic=topic, contact=contact)
        elif topic == RouterManager.topic_show_contact:
            self.handle_dest_change(1)
            self.contact_page.on_receive_show_event(topic=topic, contact=contact)

    def handle_dest_change(self, selected_index):
        page = self.page
        self.rail.selected_index = selected_index
        # 上个点击文本置灰
        dest_pre_text: text = self.rail.destinations[self.current_nail_index].label_content
        dest_pre_text.color = colors.WHITE54
        dest_pre_text.weight = FontWeight.NORMAL
        # 当前点击着重显示
        dest_current_text = self.rail.destinations[selected_index].label_content
        dest_current_text.color = colors.WHITE
        # dest_current_text.weight = FontWeight.BOLD
        dest_current_text.weight = FontWeight.NORMAL
        #
        self.current_nail_index = selected_index
        HomeStorageManager.save_homepage_index(selected_index)
        #
        self.dest_layout.controls.clear()
        self.dest_layout.controls.append(self.get_title_bar())
        self.dest_layout.controls.append(Divider(color=colors.BLACK12, height=0.5))
        if selected_index == 0:
            self.dest_layout.controls.append(self.chat_page)
            pass
        elif selected_index == 1:
            self.dest_layout.controls.append(self.contact_page)
            pass
        elif selected_index == 2:
            self.dest_layout.controls.append(self.me_page)
            pass
        elif selected_index == 3:
            self.dest_layout.controls.append(self.export_page)
            pass
        self.page.update()
        pass

    def get_title_bar(self):
        title_bar = Row(
            controls=[
                Container(width=15),
                Text("蜜蜂AI聊天记录管理 v0.1", color="#102057", size=12, weight=FontWeight.BOLD),
                Container(expand=1),
                Container(IconLocalImage("window_icon_minize.png"),
                          ink=True, padding=10, on_click=lambda e: self.window_minimized()),
                Container(IconLocalImage("window_icon_close.png"),
                          ink=True, padding=10, on_click=lambda e: self.page.window_destroy())
            ],
            spacing=0)
        return WindowDragArea(title_bar)

    def window_minimized(self):
        self.page.window_minimized = True
        self.page.update()
