from flet_core import *

from app.person import Me
from app.util.region_conversion import conversion_region_to_chinese


# 聊天记录列表item
class MeInfo(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        me = Me()
        self.bgcolor = colors.WHITE
        self.padding = 0
        # 微信头像
        self.avatar = CircleAvatar(foreground_image_src=me.smallHeadImgUrl, width=35, height=35)
        # 用户名
        self.user_name = Text(value=me.nickName, size=14, weight=FontWeight.BOLD, color=colors.BLACK, )

        # 性别
        gender_code = me.detail.get('gender')
        gender_icon = Container()
        if gender_code == 1:
            gender_icon = Icon(icons.MAN_OUTLINED, color=colors.BLUE, size=15)
        elif gender_code == 2:
            gender_icon = Icon(icons.WOMAN_OUTLINED, color=colors.RED, size=15)
        #

        # 联系人信息
        info_list = [
            f"微信id：{me.wxid}",
            f"微信号：{me.account}",
            f"地区：{conversion_region_to_chinese(me.detail.get('region'))}",
            f"昵称：{me.nickName}",
            f"邮箱：{me.mail}",
            f"电话：{me.mobile}",
            # f"标签：{contact.label_name}",
        ]
        grid_list = ListView(padding=5, spacing=2)
        for item in info_list:
            grid_list.controls.append(Text(item, color="#666666", size=13))

        # 个性签名
        signature = Container(
            Text(f"个性签名：{me.detail.get('signature')}", size=13, color=colors.BLACK54),
            bgcolor=colors.BLUE_50,
            border_radius=5,
            width=460,
            padding=padding.symmetric(8, 10),
            margin=margin.only(0, 15, 10, 0)
        )
        grid_list.controls.append(
            Row([signature])
        )

        # 总体布局
        self.content = Column(
            spacing=0,
            controls=[
                Row(
                    controls=[
                        Container(self.avatar, padding=padding.only(15, 15, 10, 0), alignment=alignment.top_left),
                        Column([
                            Container(height=2),
                            Row([gender_icon, self.user_name], spacing=0),
                            grid_list
                        ]),

                    ],
                    expand=True,
                    alignment=alignment.top_left
                )
            ])
