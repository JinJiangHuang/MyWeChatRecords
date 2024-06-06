from flet import *

from app.components.CustomButton import BigButton
from app.components.RowColumn import RowColumn
from app.page import DataManager
from app.page.exportPage.ExportChoiceItem import ExportChoiceItem
from app.page.exportPage.MsgTypes import wxMsgTypes
from app.util.exporter.output import Output


# 聊天记录列表item
class ExportConfigPage(Container):
    def __init__(self, on_click_start_btn):
        super().__init__()
        self.export_choices = {}
        self.export_type = ""
        self.padding = 0
        self.margin = 0
        self.expand = True
        self.bgcolor = colors.GREY_200
        self.on_click_start_btn = on_click_start_btn

        prompt_bar = Container(
            bgcolor="#FFF7E0",
            border_radius=10,
            width=460,
            padding=10,
            content=Text(
                color="#470606", size=12,
                value="1 、导出中途请不要关闭软件； \n2 、为保证导出顺畅，单次尽量不超过5个聊天对象",
                weight=FontWeight.BOLD
            )
        )

        # 导出格式
        export_format = Dropdown(
            value="导出为csv",
            options=[
                dropdown.Option(text="导出为csv", key="csv"),
                dropdown.Option(text="导出为html", key="html"),
                dropdown.Option(text="导出为docx", key="docx"),
                dropdown.Option(text="导出为json", key="json"),
                dropdown.Option(text="导出为txt", key="txt"),
            ],
            on_change=lambda e: self.on_export_type_change(e.control),
            content_padding=padding.symmetric(0, 15), item_height=36, height=36,
            border_color=colors.WHITE,
            border_width=0.5,
            border_radius=5,
            text_style=TextStyle(size=13, weight=FontWeight.BOLD, color="#102057"),
            bgcolor=colors.WHITE
        )
        self.checkbox_row_column = RowColumn(
            padding=0,
            controls=[ExportChoiceItem(content=key, visible=False, on_check_change=lambda e: {})
                      for (key, value) in wxMsgTypes.items()]
        )
        self.choice_container = Container(self.checkbox_row_column)

        self.choice_description = Text("已选 0 个聊天对象")
        #

        self.btn_start = BigButton(on_click=self.on_export_btn_click)
        open_dir_export_chat_history = Container(Icon(icons.FOLDER_OUTLINED, size=20),
                                                 on_click=lambda e: DataManager.open_msg_history_export_dir())

        space_item = Container(width=12)
        # 总体布局
        self.content = Column(
            spacing=0,
            controls=[
                Row(
                    controls=[
                        Container(padding=padding.only(15, 15, 10, 0), alignment=alignment.top_left),
                        Column([
                            Container(height=2),
                            Row([prompt_bar], spacing=0),
                            Row([self.labelText("导出格式"), space_item, export_format], spacing=0,
                                alignment=alignment.center_right),
                            Row([self.labelText("消息类型"), space_item, self.choice_container], spacing=0,
                                vertical_alignment=CrossAxisAlignment.START),
                            Container(height=20),
                            Row([self.labelText(""), self.choice_description]),
                            Row([self.labelText(""), self.btn_start, open_dir_export_chat_history])
                        ]),

                    ],
                    expand=True,
                    alignment=alignment.top_left
                )
            ])

    def on_export_btn_click(self, e):
        # self.btn_start.disabled = True
        self.page.update()
        callback = self.on_click_start_btn(e)

    def labelText(self, content: str):
        return Container(Text(content, size=13, color="#666666", text_align=TextAlign.RIGHT), width=90)

    def on_export_type_change(self, e):
        file_type = e.value
        print(e.value)
        self.update_export_checkbox(file_type)
        print(self.export_choices)
        self.checkbox_row_column = RowColumn(
            controls=[ExportChoiceItem(content=key, visible=self.export_choices.keys().__contains__(key),
                                       on_check_change=lambda e: {}) for (key, value) in wxMsgTypes.items()],
            padding=0
        )
        self.choice_container.content = self.checkbox_row_column
        self.choice_container.update()
        self.update()

    def update_export_checkbox(self, file_type: str):
        if file_type == 'html':
            self.export_type = Output.HTML
            self.export_choices = {"文本": True, "图片": True, "语音": False, "视频": False, "表情包": False,
                                   '音乐与音频': False, '分享卡片': False, '文件': False,
                                   '转账': False, '音视频通话': False, '拍一拍等系统消息': True}  # 定义导出的数据类型，默认全部选择
        elif file_type == 'csv':
            self.export_type = Output.CSV
            self.export_choices = {"文本": True, "图片": True, "视频": True, "表情包": True}  # 定义导出的数据类型，默认全部选择
        elif file_type == 'txt':
            self.export_type = Output.TXT
            self.export_choices = {"文本": True, "图片": True, "语音": True, "视频": True, "表情包": True,
                                   '音乐与音频': True, '分享卡片': True, '文件': True,
                                   '拍一拍等系统消息': True}  # 定义导出的数据类型，默认全部选择
        elif file_type == 'docx':
            self.export_type = Output.DOCX
            self.export_choices = {"文本": True, "图片": False, "语音": False, "视频": False,
                                   "表情包": False, '拍一拍等系统消息': True}  # 定义导出的数据类型，默认全部选择
        elif file_type == 'json':
            self.export_type = Output.JSON
            self.export_choices = {}  # 定义导出的数据类型，默认全部选择
        else:
            self.export_choices = {"文本": True, "图片": True, "视频": True, "表情包": True}  # 定义导出的数据类型，默认全部选择
