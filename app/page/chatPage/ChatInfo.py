import os.path
import traceback

from flet_core import *

from app.DataBase import msg_db, hard_link_db
from app.config import GlobalConfigs
from app.page import DataManager
from app.page.RouterManager import Router
from app.page.chatPage.ContactMenu import ContactMenu
from app.person import Contact, Me
from app.util.emoji import get_emoji
from app.util.path import get_abs_path


class ChatInfo(Column):
    def __init__(self, contact: Contact):
        super().__init__()
        self.messages: list[dict] = []
        self.last_timestamp = 0
        self.last_str_time = ''
        self.last_pos = 0
        self.contact: Contact = contact
        self.spacing = 0
        # 标题栏
        title_bar = Row(
            controls=[
                Text(self.contact.remark, size=12.5, weight=FontWeight.BOLD,
                     color="#102057", width=350, overflow=TextOverflow.ELLIPSIS),
                Container(expand=1),

                Container(Text("导出聊天记录", size=12, color=colors.BLACK87),
                          on_click=lambda e: (
                              Router().pubsub_export_chat_history(contact),

                          )),
                Container(width=4),
                Container(Icon(icons.FOLDER_OUTLINED, color=colors.BLACK, size=15, tooltip="查看导出记录"),
                          ink=True, padding=10,
                          on_click=lambda e: DataManager.open_msg_history_export_dir(contact)),
                ContactMenu(contact),

            ],
            spacing=0)
        self.controls.append(Container(title_bar, height=50, bgcolor="#F7F9FF", padding=padding.only(10, 0, 0, 0)))
        # self.controls.append(Divider(color=colors.BLACK12, height=0.5))
        #
        self.msg_list = ListView([], expand=1, padding=0)
        self.label_remark = Text(self.contact.remark)
        self.controls.append(self.msg_list)

    def did_mount(self):
        last_message_id = 9999999999
        messages = msg_db.get_message_by_num(self.contact.wxid, last_message_id)
        if messages and messages != []:
            last_message_id = messages[-1][0]
            self.messages = messages
        else:
            self.show_empty()
            return
        self.msg_list.controls.clear()
        for position, message in enumerate(messages):
            # print(f"聊天记录:{self.contact.remark}\n", message)
            self.add_message(message, position)
            pass
        self.update()
        # self.msg_list.scroll_to(key="msg_0")

    def verticalScrollBar(self, pos):
        """
        滚动条到0之后自动更新聊天记录
        :param pos:
        :return:
        """
        # print(pos)
        if pos > 0:
            return

        # 记录当前滚动条最大值
        # self.last_pos = self.chat_window.verticalScrollBar().maximum()
        # self.update_history_messages()
        pass

    def update_history_messages(self):
        self.show_chat_thread.start()

    def setScrollBarPos(self):
        """
        将滚动条位置设置为上次看到的地方
        :param pos:
        :return:
        """
        # self.chat_window.update()
        # self.chat_window.show()
        # pos = self.chat_window.verticalScrollBar().maximum() - self.last_pos
        # self.chat_window.set_scroll_bar_value(pos)
        pass

    def is_5_min(self, timestamp):
        if abs(timestamp - self.last_timestamp) > 300:
            self.last_timestamp = timestamp
            return True
        return False

    def get_display_name(self, is_send, message) -> str:
        if self.contact.is_chatroom:
            if is_send:
                display_name = Me().name
            else:
                display_name = message[13].remark
        else:
            display_name = None
        return display_name

    def show_empty(self):
        item = Row(
            controls=[
                Text("无聊天记录", color=colors.BLACK38, size=12, expand=1, text_align=TextAlign.CENTER)],
            expand=1,
            alignment=alignment.center)
        self.msg_list.controls.clear()
        self.msg_list.controls.insert(0, Container(item, padding=padding.symmetric(20, 0)))
        self.update()

    def add_message(self, message, position):
        try:
            # print("\r\n--------------------------------------")
            type_ = message[2]
            str_content = message[7]
            str_time = message[8]
            # print(type_, type(type_))
            is_send = message[4]
            avatar = DataManager.get_msg_avatar_path(is_send, message=message, contact=self.contact,
                                                     is_absolute_path=True)
            display_name = self.get_display_name(is_send, message)
            timestamp = message[5]
            BytesExtra = message[10]

            # print("[时间]：", str_time)
            # print("[头像]：", avatar)
            # print("[名称]", display_name)
            # print(f"[is_send]：{is_send}")
            # print("[内容]", str_content)
            # print("[内容类型]", type_)
            # print("[BytesExtra]", BytesExtra)
            # print("[timestamp]", timestamp)

            avatar1 = CircleAvatar(background_image_src=avatar, bgcolor=colors.BLACK38)
            space_item = Container(width=30)
            bg_color_content = "#3C77FE" if is_send else "#F7F7F7"

            text_color = "#ffffff" if is_send else colors.BLACK87
            control_content = Text(str_content, color=text_color, size=13)
            if type_ == 1:
                # print(type_, str_content)
                pass
            elif type_ == 3:
                image_path = hard_link_db.get_image(content=str_content, bytesExtra=BytesExtra, up_dir=Me().wx_dir,
                                                    thumb=False)
                # print(type_, image_path)
                output_path = os.path.join(GlobalConfigs().path_export_dir, self.contact.get_uniquid_name(), "image")
                os.makedirs(output_path, exist_ok=True)
                image_path = get_abs_path(image_path, output_path)
                print("图片", output_path, image_path)
                control_content = Image(width=200, height=100, src=image_path)
            elif type_ == 47:
                image_path = get_emoji(str_content, thumb=True)
                # print(type_, image_path)
                control_content = Image(width=100, height=100, src=image_path)
            elif type_ == 10000:
                str_content = str_content.lstrip('<revokemsg>').rstrip('</revokemsg>')
                # print(type_, str_content)
                control_content = Text(str_content)

            item = ListTile(
                key=f"msg_{position}",
                title_alignment=ListTileTitleAlignment.TOP,
                leading=avatar1 if not is_send else space_item,
                trailing=avatar1 if is_send else space_item,
                title=Container(control_content, padding=8, border_radius=5, bgcolor=bg_color_content)
            )
            # self.msg_list.controls.insert(0, Row([Container(Text(str_content), bgcolor=colors.GREEN_50)]))
            # self.msg_list.controls.insert(0, Text(display_name))
            # self.msg_list.controls.insert(0, Row([Text(is_send), CircleAvatar(foreground_image_src=avatar, bgcolor=colors.RED)]))
            self.msg_list.controls.insert(0, item)
            self.msg_list.controls.insert(0, Row([Text(str_time, color=colors.BLACK38, size=12, expand=1,
                                                       text_align=TextAlign.CENTER)], expand=1,
                                                 alignment=alignment.center))
            # if type_ == 1:
            #     if self.is_5_min(timestamp):
            #         time_message = Text(self.last_str_time)
            #         self.last_str_time = str_time
            #         self.msg_list.controls.insert(0, time_message)
            #     bubble_message = BubbleMessage(
            #         str_content,
            #         avatar,
            #         type_,
            #         is_send,
            #         display_name=display_name
            #     )
            #     self.msg_list.controls.insert(0, bubble_message)
            # elif type_ == 3:
            #     # return
            #     if self.is_5_min(timestamp):
            #         time_message = Text(self.last_str_time)
            #         self.last_str_time = str_time
            #         self.msg_list.controls.insert(0, time_message)
            #     image_path = hard_link_db.get_image(content=str_content, bytesExtra=BytesExtra, up_dir=Me().wx_dir,thumb=False)
            #     image_path = get_abs_path(image_path)
            #     bubble_message = BubbleMessage(
            #         image_path,
            #         avatar,
            #         type_,
            #         is_send
            #     )
            #     self.msg_list.controls.insert(0, bubble_message)
            # elif type_ == 47:
            #     return
            #     if self.is_5_min(timestamp):
            #         time_message = Notice(self.last_str_time)
            #         self.last_str_time = str_time
            #         self.msg_list.controls.insert(0,time_message)
            #     image_path = get_emoji(str_content, thumb=True)
            #     bubble_message = BubbleMessage(
            #         image_path,
            #         avatar,
            #         3,
            #         is_send
            #     )
            #     self.msg_list.controls.insert(0,bubble_message)
            # elif type_ == 10000:
            #     str_content = str_content.lstrip('<revokemsg>').rstrip('</revokemsg>')
            #     message = Text(str_content)
            #     self.msg_list.controls.insert(0,message)
        except:
            print(message)
            traceback.print_exc()
