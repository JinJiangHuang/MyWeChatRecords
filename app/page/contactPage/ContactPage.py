import threading
import time
from typing import Optional

from flet import *

from app.components.PromptDialog import PromptDialog
from app.page import RouterManager
from app.page.DataManager import WxDataManager
from app.page.RouterManager import Router
from app.page.StoreManager import ContactStorageManager
from app.page.contactPage.ContactInfo import ContactInfo
from app.page.contactPage.ContactItem import ContactItem
from app.person import Contact


# 聊天界面，包含聊天记录列表和聊天详情窗口
class ContactPage(Row):
    """
    @Author  : youngwm
    @Time    : 2024/5/6
    @IDE     : Pycharm
    @Version : Python3.10
    @comment : ···
    """
    def __init__(self):
        super().__init__()
        #
        self.listview_last_position = -1
        self.contact_list: list[Contact] = []
        self.spacing = 0
        self.expand = True
        #
        self.current_selected_index = 0
        #
        self.running = False
        self.search_bar = None
        self.contact_listview: Optional[ListView] = None
        self.user_header = None
        self.user_name = None
        self.user_layout = None
        self.layout_contact_list: Optional[Container] = None
        self.layout_contact_detail: Optional[Container] = None

        self.init_chat_list()
        self.init_chat_detail()

        self.controls.clear()
        self.controls.append(self.layout_contact_list)
        self.controls.append(VerticalDivider(color=colors.BLACK12, width=0.7))
        self.controls.append(self.layout_contact_detail)

    def did_mount(self):
        if self.listview_last_position > 0:
            self.contact_listview.scroll_to(offset=self.listview_last_position, duration=0)
        if self.running:
            return
        self.current_selected_index = ContactStorageManager.get_contact_page_index()
        if not self.current_selected_index:
            self.current_selected_index = 0
        th = threading.Thread(target=self.load_and_update_contact_list, args=(), daemon=True)
        th.start()
        pass

    def load_and_update_contact_list(self):
        self.contact_list = WxDataManager().get_contact_list()
        if len(self.contact_list) == 0:
            Router().go_load_page()
            PromptDialog().show(self.page, "数据为空，请重新加载")
            return
        self.update_contact_list()
        self.running = len(self.contact_list) > 0
        show_contact = self.contact_list[self.current_selected_index]
        self.on_receive_show_event(RouterManager.topic_show_contact, show_contact)

    def update_contact_list(self):
        for i, contact in enumerate(self.contact_list):
            # Container/ Column / [2] ListView / ChatListItem
            chat_item = ContactItem(contact,
                                    on_click=lambda e, index=i, c=contact: {self.on_click_contact_item(index=index, contact=c)})
            chat_item.key = contact.wxid
            self.contact_listview.controls.append(chat_item)
            if i == self.current_selected_index:
                # print("chat当前选中索引", self.current_selected_index)
                self.on_click_contact_item(index=i, contact=contact)
        self.update()
        pass

    def on_click_contact_item(self, contact: Contact, index: int = None):
        print("点击", contact.nickName)
        if index == None:
            index = self.contact_list.index(contact)
        print("点击", contact.remark)
        # 重置上一个item的选中状态
        self.set_chat_list_item_check_ui(self.current_selected_index, False)
        self.set_chat_list_item_check_ui(index, True)
        # 记录选中状态
        self.current_selected_index = index
        ContactStorageManager.save_contact_page_index(index)
        # 更新详情显示
        chat_info = ContactInfo(contact)
        self.layout_contact_detail.content = chat_info
        self.update()

    def set_chat_list_item_check_ui(self, position, is_check):
        # Container/ Column / [1] ListView / ChatListItem
        listview = self.layout_contact_list.content.controls[1]
        if len(listview.controls) > position:
            chat_list_item = listview.controls[position]
            if isinstance(chat_list_item, ContactItem):
                chat_list_item.set_checked(is_check)
            pass

    def init_chat_list(self):
        # 用户

        self.user_header = CircleAvatar(width=52, height=52, bgcolor=colors.GREEN_50)
        self.user_name = Text(size=14, color=colors.BLACK54, value="蜜蜂AI")
        self.user_layout = Row(
            [
                self.user_header,
                Column([self.user_name], spacing=0)
            ],
        )

        # 02-01 搜索框
        self.search_bar = SearchBar(bar_hint_text="搜索", expand=1,
                                    bar_bgcolor=colors.WHITE,
                                    bar_overlay_color=colors.WHITE,
                                    view_hint_text="输入关键词，点击Enter键搜索",
                                    view_hint_text_style=TextStyle(size=14, weight=FontWeight.NORMAL,
                                                                   color=colors.BLACK38),
                                    view_header_text_style=TextStyle(size=14, weight=FontWeight.NORMAL,
                                                                     color=colors.BLACK87),
                                    view_bgcolor=colors.WHITE,
                                    view_surface_tint_color=colors.WHITE,
                                    view_elevation=4,
                                    view_side=BorderSide(color=colors.GREY_200, width=0.5),
                                    on_submit=lambda e: self.handle_search_change(self.search_bar.value),
                                    height=30,
                                    divider_color=colors.GREY_50,
                                    controls=[]
                                    )
        location_current = Container(Icon(icons.MY_LOCATION, size=15), padding=5, visible=False,
                                     on_click=lambda e: {
            self.scroll_to_contact(self.contact_list[self.current_selected_index])
        })
        search_row = Row([self.search_bar, location_current], expand=1, spacing=5)

        # 03-01 标题
        self.contact_listview = ListView(expand=True, spacing=0, cache_extent=True,
                                         on_scroll=lambda e: {
                                             self.on_listview_scroll(e)
                                         })

        # 03- 操作栏
        self.layout_contact_list = Container(
            content=Column(
                controls=[
                    Container(search_row, padding=padding.symmetric(horizontal=15, vertical=5)),
                    self.contact_listview,
                ]
            ),
            bgcolor=colors.WHITE,
            padding=padding.only(0, 0, 0, 0),
            margin=margin.Margin(0, 0, 0, 0),
            border_radius=0,
            width=230,
        )

    def on_listview_scroll(self, event: OnScrollEvent):
        if event.event_type == 'end':
            self.listview_last_position = event.pixels

    def handle_search_focus_change(self):
        pass

    def init_chat_detail(self):
        self.layout_contact_detail = Container(expand=True, padding=0, margin=0, bgcolor=colors.WHITE)

    def on_receive_show_event(self, topic, contact):
        if topic == RouterManager.topic_show_contact:
            if contact:
                print("显示一个联系人信息，滚动到key=", contact.wxid)
                index = self.contact_list.index(contact)
                self.on_click_contact_item(index=index, contact=contact)
                self.scroll_to_contact(contact)

    def scroll_to_contact(self, contact: Contact):
        index = self.contact_list.index(contact)
        if len(self.contact_listview.controls) > index:
            item_height = self.contact_listview.controls[index].height
            self.contact_listview.scroll_to(offset=item_height * index, duration=200)

    def handle_search_change(self, keyword: str, update_ui=True):
        if not self.running:
            return
        contact_list_valid = self.contact_list
        controls = [ContactItem(contact, on_click=lambda e, c=contact: {
            self.on_click_contact_item(contact=c),
            self.search_bar.close_view(),
            self.scroll_to_contact(c),
            self.handle_search_change("", update_ui=False)  # 初始化搜索框中内容
        })
                    for contact in contact_list_valid if
                    (keyword in contact.nickName
                     or keyword in contact.remark
                     or keyword in contact.wxid
                     )]
        self.search_bar.controls = controls
        self.search_bar.update()
        if update_ui:
            self.search_bar.close_view(keyword)
            time.sleep(0.001)
            self.search_bar.open_view()
        pass
