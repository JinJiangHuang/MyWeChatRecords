import threading
import time
from typing import Optional

from flet import *

from app.components.LoadingDialog import LoadingDialog
from app.components.PromptDialog import PromptDialog
from app.page import RouterManager
from app.page.DataManager import WxDataManager
from app.page.RouterManager import Router
from app.page.contactPage.ContactItem import ContactItem
from app.page.exportPage.ContactExportItem import ContactExportItem
from app.page.exportPage.ExportConfigPage import ExportConfigPage
from app.page.exportPage.MsgTypes import wxMsgTypes
from app.person import Contact
from app.util.exporter.output import Output


# 聊天界面，包含聊天记录列表和聊天详情窗口
class ExportPage(Row):
    def __init__(self):
        super().__init__()
        #
        self.listview_last_position = -1
        self.contact_list: list[Contact] = []
        self.contact_list_select: list[Contact] = []
        self.contact_index_list_select: list[int] = []
        self.last_click_contact_index = 0
        self.select_all_is_running = False
        self.spacing = 0
        self.expand = True
        #
        self.running = False
        self.search_bar = None
        self.contact_listview: Optional[ListView] = None
        self.user_header = None
        self.user_name = None
        self.user_layout = None
        self.layout_contact_list: Optional[Container] = None
        self.layout_export_config: Optional[Container] = None
        self.export_config_page = ExportConfigPage(on_click_start_btn=lambda e: self.export_data())

        self.init_chat_list()
        self.init_chat_detail()

        divider = VerticalDivider(color=colors.BLACK12, width=0.7)
        self.controls.clear()
        self.controls.append(self.layout_contact_list)
        self.controls.append(divider)
        self.controls.append(self.layout_export_config)

    def did_mount(self):
        if self.listview_last_position > 0:
            self.contact_listview.scroll_to(offset=self.listview_last_position, duration=0)
        if self.running:
            return
        th = threading.Thread(target=self.load_and_update_contact_list, args=(), daemon=True)
        th.start()

    def on_receive_export_event(self, topic, contact):
        if topic == RouterManager.topic_export_chat_history:
            self.contact_list_select.clear()
            self.contact_index_list_select.clear()
            if contact:
                print("选中一个联系人")
                self.deselect_all_contact(contact)
                self.scroll_to_contact(contact)
            else:
                print("选中所有联系人")
                self.select_all_contact()

    def scroll_to_contact(self, contact: Contact):
        index = self.contact_list.index(contact)
        if len(self.contact_listview.controls) > index:
            item_height = self.contact_listview.controls[index].height
            self.contact_listview.scroll_to(offset=item_height * index, duration=200)

    def scroll_to_next_contact(self, reverse=False):
        index = self.last_click_contact_index
        len_select = len(self.contact_index_list_select)
        print("当前位置", index)
        if len_select > 0:
            index_last = self.contact_index_list_select[len_select-1]
            print("最大选中位置", index, index_last)
            if index >= index_last:
                index = 0

        print("推理最后点击位置", index)
        for i, select_index in enumerate(self.contact_index_list_select):
            if index < select_index:
                self.last_click_contact_index = select_index
                contact = self.contact_list_select[i]
                print("滚动到", select_index, contact.remark)
                self.scroll_to_contact(contact)
                return
        pass

    def load_and_update_contact_list(self):
        self.contact_list = WxDataManager().get_contact_list()
        if len(self.contact_list) == 0:
            Router().go_load_page()
            PromptDialog().show(self.page, "数据为空，请重新加载")
            return
        self.update_contact_list()
        self.running = len(self.contact_list) > 0

    def update_contact_list(self):
        for i, contact in enumerate(self.contact_list):
            # Container/ Column / [2] ListView / ChatListItem
            chat_item = ContactExportItem(contact,
                                          on_check_change=lambda is_select, index=i, c=contact: {
                                              self.on_select_contact_item(index, c, is_select)
                                          }
                                          )
            self.contact_listview.controls.append(chat_item)
        self.update()
        pass

    # 全选应用列表
    def select_all_contact(self):
        for item in self.contact_listview.controls:
            if isinstance(item, ContactExportItem):
                item.set_checked(True)
                if self.running:
                    item.update()
        self.contact_listview.update()

    # 取消全选
    def deselect_all_contact(self, contact: Contact = None):
        for item in self.contact_listview.controls:
            if isinstance(item, ContactExportItem):
                check = item.contact == contact
                item.set_checked(check)
                if self.running:
                    item.update()
        self.contact_listview.update()

    def select_all_toggle(self):
        if self.select_all_is_running:
            return
        self.select_all_is_running = True
        deselect_all = len(self.contact_list) <= len(self.contact_index_list_select)
        if deselect_all:
            self.deselect_all_contact()
        else:
            self.select_all_contact()
        self.select_all_is_running = False

    def on_select_contact_item(self, index, contact: Contact, is_select):
        # print("选中", contact.remark, is_select)
        # 记录选中状态
        self.last_click_contact_index = index
        if is_select:
            self.contact_list_select.append(contact)
            self.contact_index_list_select.append(index)
        elif self.contact_list_select.__contains__(contact):
            self.contact_list_select.remove(contact)
            self.contact_index_list_select.remove(index)
        len_select = len(self.contact_list_select)
        # print("已选中联系人数", len_select)
        self.export_config_page.choice_description.value = f"已选 {len_select} 个聊天对象"
        self.export_config_page.update()

    def export_data(self):
        loading = LoadingDialog()

        def export_finish(index, len):
            if index < len - 1:
                return
            loading.dismiss()
            PromptDialog().show(self.page, "导出完成")

        export_config_page = self.export_config_page
        # 在这里获取用户选择的导出数据类型
        selected_types = {wxMsgTypes[export_type] for export_type in export_config_page.export_choices.keys()}
        len_contact = len(self.contact_list_select)
        if len_contact == 0:
            PromptDialog().show(self.page, "请勾选导出联系人")
            return
        # 在这里根据用户选择的数据类型执行导出操作
        print("导出配置界面-选择的数据类型:", export_config_page.export_type)
        if export_config_page.export_type == '':
            PromptDialog().show(self.page, "请选择导出格式")
            return
        for i, contact in enumerate(self.contact_list_select):
            print("导出聊天记录", contact.remark)
            loading.show(self.page, f"{i + 1}/{len_contact}数据导出中..")
            worker = Output(contact, type_=export_config_page.export_type, message_types=selected_types,
                            on_export_finish=lambda e, index=i: {export_finish(index, len_contact)})

    def init_chat_list(self):
        # 用户

        user_avatar = CircleAvatar(width=52, height=52, bgcolor=colors.GREEN_50, visible=False)
        self.user_name = Text(size=16, weight=FontWeight.BOLD, color="#102057", value="选择导出聊天对象")
        self.user_layout = Row(
            [
                user_avatar,
                Column([self.user_name], spacing=0)
            ],
        )

        # 02-01 搜索框
        self.search_bar = SearchBar(bar_hint_text="搜索", expand=1,
                                    bar_bgcolor=colors.WHITE,
                                    bar_overlay_color=colors.WHITE,
                                    view_hint_text="输入关键词，点击Enter键搜索",
                                    view_hint_text_style=TextStyle(size=12.5, weight=FontWeight.NORMAL,
                                                                   color=colors.BLACK38),
                                    view_header_text_style=TextStyle(size=12.5, weight=FontWeight.NORMAL,
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
            self.scroll_to_next_contact()
        })
        select_all = Container(Icon(icons.CHECK_OUTLINED, size=15), padding=5, on_click=lambda e: {
            self.select_all_toggle()
        })
        search_row = Row([self.search_bar, Container(width=10), location_current, select_all], expand=1, spacing=0)

        # 03-01 标题
        self.contact_listview = ListView(expand=True, spacing=0, cache_extent=True,
                                         on_scroll=lambda e: {
                                             self.on_listview_scroll(e)
                                         })

        # 03- 操作栏
        self.layout_contact_list = Container(
            content=Column(
                controls=[
                    Container(self.user_layout, padding=padding.symmetric(horizontal=15, vertical=5)),
                    Container(search_row, padding=padding.symmetric(horizontal=15, vertical=5)),
                    self.contact_listview,
                ]
            ),
            bgcolor=colors.GREY_50,
            padding=padding.only(0, 0, 0, 0),
            margin=margin.Margin(0, 0, 0, 0),
            border_radius=0,
            width=300,
        )

    def on_listview_scroll(self, event: OnScrollEvent):
        if event.event_type == 'end':
            self.listview_last_position = event.pixels

    def handle_search_change(self, keyword: str, update_ui=True):
        if not self.running:
            return
        contact_list_valid = self.contact_list
        controls = [ContactItem(contact, on_click=lambda e, c=contact: {
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

    def handle_search_focus_change(self):
        pass

    def init_chat_detail(self):
        self.layout_export_config = Container(expand=True, padding=0, margin=0, bgcolor=colors.GREY_200)
        self.layout_export_config.content = self.export_config_page
