import math

import flet as ft
from flet_core import *

from app import config
from app.components.FletCommonUi import fletCommonUi
from app.components.PrivacyCheckView import PrivacyCheckView
from app.components.PromptDialog import PromptDialog
from app.config import UrlConfigs
from app.page import RouterManager as RouterManager
from app.page.LoadPage.ItemText import ItemTextList
from app.page.LoadPage.LoadingBtn import LoadingBtn


class LoadWechatDataPage(Container):

    def __init__(self):
        super().__init__()
        # flet PC应用相关配置
        self.padding = padding.symmetric(horizontal=20, vertical=10)
        self.width = 1500
        self.height = 1200
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=Alignment(0.8, 1),
            colors=[
                "0xffcde1fc",
                "0xffbfd8fb",
                "0xfff5f8fd",
                "0xffffffff",
                "0xffffffff",
            ],
            tile_mode=ft.GradientTileMode.MIRROR,
            rotation=math.pi / 3,
        )
        #
        self.max_task = 1

        close_btn = IconButton(icon=icons.CLOSE_OUTLINED, on_click=lambda _: RouterManager.Router().go_home_page())
        self.loading_button = LoadingBtn(
            width=200,
            content=f"立即开始",
            loading_prompt=f"加载中..",
            on_click=lambda e: {self.on_start_loading()},
            on_loading_finish=lambda result: {self.on_loading_finish(result)},
            on_get_max_task=lambda task_num: {self.on_get_max_task(task_num)},
            on_task_finish=lambda task_order: {self.on_task_finish(task_order)},
            on_task_error=lambda task_order: {self.on_task_error(task_order)},
            on_all_task_success=lambda: {self.on_all_task_success()},
        )
        self.progressBar = ProgressBar(visible=False, width=500)
        self.show_config = Text(no_wrap=True, visible=False)
        #
        self.is_agree_privacy = False
        self.privacyCheckView = PrivacyCheckView(
            on_check_change=lambda e: self.on_privacy_check_change(e),
            on_click_privacy=lambda e: UrlConfigs.open_url_privacy(),
            on_click_service=lambda e: UrlConfigs.open_url_service_items(),
            on_click_github_url=lambda e: UrlConfigs.open_url_github_from(),
        )
        content_layout = Column(
            controls=[
                Row(
                    [Container(width=550), close_btn, ], spacing=0
                ),
                Image(width=498 / 1.5, height=154 / 1.5, src=config.get_local_image_file_path("page_export_title.png")),
                Container(height=20),
                Text("为管理尽可能完整的聊天记录，请确保已完成", color=colors.BLACK, weight=FontWeight.BOLD, size=18),
                ItemTextList(),
                Container(height=20),
                self.loading_button,
                self.progressBar,
                self.show_config,
                Container(height=8),
                self.privacyCheckView,
                Text("", expand=1, no_wrap=False)
            ],
            spacing=10
        )
        self.content = WindowDragArea(
            Row(
                [
                    Container(width=240),
                    content_layout,
                ]
            )
        )

    def did_mount(self):
        flet_app_config = {
            "width": 400,
            "height": 500,
            "rootBg": "grey200",
            "title": "加载/更新聊天记录",
        }
        page = self.page
        page.title = flet_app_config['title']
        page.bgcolor = flet_app_config['rootBg']
        page.padding = 0
        page.spacing = 0

    def on_start_loading(self):
        if not self.is_agree_privacy:
            PromptDialog().show(self.page, "需阅读并勾选同意隐私协议和用户协议")
            return
        self.loading_button.start_process()
        progressBar = self.progressBar
        show_config = self.show_config
        self.loading_button.visible = False
        progressBar.visible = True
        self.show_config.visible = True
        progressBar.value = None
        show_config.value = "加载账号信息.."
        self.page.update()

    def on_loading_finish(self, result):
        progressBar = self.progressBar
        show_config = self.show_config
        # self.loading_button.visible = True
        # progressBar.visible = False
        show_config.value = f"\n加载到配置：{result}"
        self.page.update()

    def on_get_max_task(self, task_num):
        progressBar = self.progressBar
        show_config = self.show_config
        # progressBar.visible = True
        # self.loading_button.visible = False
        print("任务总数", task_num)
        self.max_task = task_num
        show_config.value = f"\n开始导出微信聊天记录数据库.."
        show_config.value = f"\n任务数：{task_num}"
        self.page.update()
        pass

    def on_task_finish(self, task_order):
        # print("任务结束回调", task_order)
        progressBar = self.progressBar
        progressBar.value = task_order / self.max_task
        self.show_config.value = f"数据加载进度：{task_order}/{self.max_task}"
        self.page.update()
        pass

    def on_task_error(self, task_order):
        # print("任务出错回调", task_order)
        pass

    def on_all_task_success(self, ):
        print("所有任务完成")
        progressBar = self.progressBar
        show_config = self.show_config
        progressBar.value = 1
        progressBar.visible = False
        self.show_config.visible = False
        self.loading_button.visible = True
        show_config.value = f"\n微信聊天记录数据库导出完成"
        self.page.update()
        fletCommonUi.show_snack_bar(page=self.page, msg="更新聊天记录成功！")
        RouterManager.Router().go_home_page()
        pass

    def on_privacy_check_change(self, is_check):
        # print("用户同意隐私协议", event.__dict__)
        print("用户同意隐私协议",is_check)
        self.is_agree_privacy = is_check
        pass

