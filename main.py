import json
import os

import flet as ft
from flet import *

from app import DataBase, config
from app.config import GlobalConfigs
from app.page import RouterManager, DataManager
from app.page.LoadPage.LoadDataPage import LoadWechatDataPage
from app.page.RouterManager import Router
from app.page.StoreManager import StoreGlobalManager, HomeStorageManager
from app.page.homePage.HomePage import HomePage
from app.person import Me


class Main:
    def __init__(self, page: ft.Page):
        #
        self.page = page
        page.fonts = {
            "微软雅黑": config.get_local_font_file_path("msyhl.ttc")
        }
        page.theme = Theme(font_family="微软雅黑")
        self.page.bgcolor = colors.GREY_50
        self.page.window_width = 900
        self.page.window_height = 600
        self.is_need_load_data = True
        StoreGlobalManager().init(page)
        current_usr_wxid = HomeStorageManager().get_wx_save_dir()
        print("初始化配置", current_usr_wxid)
        if current_usr_wxid:
            GlobalConfigs().update_user_wxid(current_usr_wxid)
        DataBase.init_db()
        RouterManager.Router().set_page(page)  # 必须：初始化路由中的page对象
        page.on_route_change = self.route_change
        Router().go_home_page()
        DataManager.check_wx_is_login(page)
        #
        page.window_prevent_close = True
        page.on_window_event = lambda event: {
            self.on_on_window_event(event)
        }

    def on_on_window_event(self, event):
        print(event.data)
        if event.data == "close":
            if self.page.route == RouterManager.path_load_data_page:
                Router().go_home_page()
            # else:
            #     self.page.window_close()

    def route_change(self, route):
        print("跳转路由", route)
        page = self.page
        page.views.clear()

        if page.route == RouterManager.path_root:  # 首页
            if self.is_need_load_data:
                self.load_data()
            page.views.append(
                ft.View(
                    RouterManager.path_root,
                    [
                        HomePage()
                    ],
                    padding=0
                )
            )
            pass
        elif page.route == RouterManager.path_load_data_page:  # 更新加载微信数据
            self.is_need_load_data = True
            page.views.append(View(
                route=RouterManager.path_reset_password,
                padding=0,
                controls=[
                    LoadWechatDataPage()
                ]
            ))
            pass
        elif page.route == RouterManager.path_register:  # 显示注册界面
            pass
        elif page.route == RouterManager.path_login:  # 显示登录界面
            pass
        elif page.route == RouterManager.path_reset_password:  # 显示重置密码界面
            pass
        page.update()

    def load_data(self):
        print("main 初始化数据库")
        DataBase.init_db()
        configs = GlobalConfigs()
        path_user_info_file = configs.path_user_info_file
        if os.path.exists(path_user_info_file):
            with open(path_user_info_file, 'r', encoding='utf-8') as f:
                dic = json.loads(f.read())
                wxid = dic.get('wxid')
                if wxid:
                    me = Me()
                    me.wxid = dic.get('wxid')
                    me.account = dic.get('account')
                    me.name = dic.get('name')
                    me.nickName = dic.get('name')
                    me.remark = dic.get('name')
                    me.mobile = dic.get('mobile')
                    me.mail = dic.get('mail')
                    me.wx_dir = dic.get('wx_dir')
                    me.token = dic.get('token')
                    me.acc = dic.get('token')
                    self.update_wx_account_info(wxid)
        else:
            pass

    def update_wx_account_info(self, wxid):
        from app.DataBase import micro_msg_db, misc_db, close_db
        img_bytes = misc_db.get_avatar_buffer(wxid)
        if not img_bytes:
            return
        if img_bytes[:4] == b'\x89PNG':
            # self.avatar.loadFromData(img_bytes, format='PNG')
            pass
        else:
            # self.avatar.loadFromData(img_bytes, format='jfif')
            pass
        contact_info_list = micro_msg_db.get_contact_by_username(wxid)
        if not contact_info_list:
            close_db()
            import shutil
            try:
                pass
                shutil.rmtree(GlobalConfigs().path_database_dir)
            except:
                pass
            # QMessageBox.critical(self, "数据库错误", "数据库错误，请删除app文件夹后重启电脑再运行软件")
            return
        me = Me()
        me.set_avatar(img_bytes)
        me.smallHeadImgUrl = contact_info_list[7]
        print("更新微信账号用户信息", str(me.__dict__))
        # self.avatar.foreground_image_src = me.smallHeadImgUrl
        self.page.update()


ft.app(target=Main, view=ft.AppView.FLET_APP)
