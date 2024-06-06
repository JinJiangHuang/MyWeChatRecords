from flet import *

from app.components.ChipBtn import ChipBtn
from app.components.LocalImage import LocalImage
from app.components.RowColumn import RowColumn
from app.page import DataManager
from app.page.RouterManager import Router
from app.person import Contact
from app.util.region_conversion import conversion_region_to_chinese


# 聊天记录列表item
class ContactInfo(Container):
    def __init__(self, contact: Contact):
        super().__init__()
        self.padding = 0
        self.margin = 0
        self.expand = True
        self.contact = contact
        # 微信头像
        self.avatar = CircleAvatar(foreground_image_src=contact.smallHeadImgUrl, width=35, height=35)
        # 用户名
        self.user_name = Text(value=contact.nickName, size=14, weight=FontWeight.BOLD, color=colors.BLACK, )

        # 性别
        gender_code = contact.detail.get('gender')
        gender_icon = Container()
        if gender_code == 1:
            gender_icon = Icon(icons.MAN_OUTLINED, color=colors.BLUE, size=15)
        elif gender_code == 2:
            gender_icon = Icon(icons.WOMAN_OUTLINED, color=colors.RED, size=15)
        #
        friendMomentBg = contact.detail.get('friendMomentBg')
        # print("朋友圈背景图", contact.remark, friendMomentBg)

        # 聊天记录入口
        chat_history = Container(
            content=Row([
                Container(width=360),
                LocalImage("contact_icon_chat_history.png", width=14, height=13),
                Text("聊天记录", size=12, color=colors.BLACK, ),
            ]),
            on_click=lambda e: Router().pubsub_show_chat(contact),
        )

        # 联系人信息
        info_list = [
            f"微信号：{contact.alias}",
            f"地区：{conversion_region_to_chinese(contact.detail.get('region'))}",
            f"昵称：{contact.nickName}",
            f"备注：{contact.remark}",
            f"电话：{contact.detail.get('telephone')}",
            f"标签：{contact.label_name}",
        ]
        grid_list = ListView(padding=5, spacing=2)
        for item in info_list:
            grid_list.controls.append(Text(item, color="#666666", size=13))

        # 个性签名
        signature = Container(
            Text(f"个性签名：{contact.detail.get('signature')}",
                 size=13, color="#102057"),
            bgcolor="#F3F5FA",
            border_radius=5,
            width=460,
            padding=padding.symmetric(8, 12),
            margin=margin.only(0, 15, 0, 0)
        )
        grid_list.controls.append(
            Row([signature])
        )

        # 分析聊天记录
        export_chat_history = Container(Text("", size=14, weight=FontWeight.BOLD, color=colors.BLACK),
                                        padding=padding.only(0, 18, 0, 8))
        grid_list.controls.append(export_chat_history)
        #
        export_chat_history = ChipBtn("contact_icon_export.png", "导出聊天记录",
                                      on_click=lambda e: {
                                          Router().pubsub_export_chat_history(contact)
                                      })
        open_dir_export_chat_history = ChipBtn("contact_icon_open_dir.png", "打开导出目录",
                                               on_click=lambda e: DataManager.open_msg_history_export_dir(contact))
        btn_tong_ji = ChipBtn("contact_icon_stat.png", "统计信息",
                              on_click=lambda e: DataManager.stat_analysis(contact))
        export_year_report = ChipBtn("contact_icon_year_report.png", "年度报告",
                                     on_click=lambda e: DataManager.year_report(contact))
        btn_qing_gan_fenxi = ChipBtn("contact_icon_motion.png", "AI情感分析", opacity=0.5)
        export_layout = RowColumn(
            controls=[
                export_chat_history, open_dir_export_chat_history, btn_tong_ji, export_year_report, btn_qing_gan_fenxi
            ], row_num=4
        )
        grid_list.controls.append(export_layout)

        # 总体布局
        self.content = Column(
            spacing=0,
            controls=[
                Row(
                    controls=[
                        Container(self.avatar, padding=padding.only(15, 15, 10, 0), alignment=alignment.top_left),
                        Column([
                            Container(height=12),
                            Row([gender_icon, self.user_name], spacing=0),
                            Row([chat_history, Container(width=30)], spacing=0, alignment=alignment.center_right),
                            grid_list
                        ]),

                    ],
                    spacing=0,
                    expand=True,
                    alignment=alignment.top_left
                )
            ])
