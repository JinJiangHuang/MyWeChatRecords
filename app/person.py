"""
定义各种联系人
"""
import json
import os.path
import re
from typing import Dict

import requests

from app.config import GlobalConfigs


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


class Person:
    def __init__(self):
        self.avatar_path = None
        self.avatar = None
        # self.avatar_path_qt = Icon.Default_avatar_path
        self.detail = {}

    def set_avatar(self, img_bytes):
        if not img_bytes:
            # self.avatar.load(Icon.Default_avatar_path)
            return
        # self.avatar = img_bytes
        # if img_bytes[:4] == b'\x89PNG':
        #     self.avatar.loadFromData(img_bytes, format='PNG')
        # else:
        #     self.avatar.loadFromData(img_bytes, format='jfif')

    def save_avatar(self, path=None):
        if path:
            save_path = path
            if os.path.exists(save_path):
                self.avatar_path = save_path
                return save_path
        else:
            os.makedirs(f'{GlobalConfigs().path_data_dir}/avatar', exist_ok=True)
            save_path = os.path.join(GlobalConfigs().path_data_dir, 'avatar', self.wxid + '.png')
        self.avatar_path = save_path
        if not os.path.exists(save_path):
            # self.avatar.save(save_path)
            # self.save_image_from_url(self., save_path)
            print('保存头像', save_path)

    def save_image_from_url(self, url, save_path):
        try:
            response = requests.get(url)
            response.raise_for_status()  # 确认请求成功

            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved to {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download image from {url}: {e}")


@singleton
class Me(Person):
    def __init__(self):
        super().__init__()
        self.avatar = None
        self.avatar_path = ''
        self.wxid = ''
        self.account = ''
        self.wx_dir = ''
        self.name = ''
        self.mobile = ''
        self.mail = ''
        self.smallHeadImgUrl = ''
        self.nickName = self.name
        self.remark = self.nickName
        self.token = ''

    def save_info(self):
        configs = GlobalConfigs()
        if os.path.exists(configs.path_user_info_file):
            with open(configs.path_user_info_file, 'r', encoding='utf-8') as f:
                info_data = json.loads(f.read())
            info_data['name'] = self.name
            info_data['mobile'] = self.mobile
            with open(configs.path_user_info_file, 'w', encoding='utf-8') as f:
                json.dump(info_data, f, ensure_ascii=False, indent=4)

    def save_avatar(self, path=None):
        if path:
            save_path = path
            if os.path.exists(save_path):
                self.avatar_path = save_path
                return save_path
        else:
            os.makedirs('avatar', exist_ok=True)
            save_path = os.path.join(f'data/avatar/', self.wxid + '.png')
        self.avatar_path = save_path
        if not os.path.exists(save_path):
            # self.avatar.save(save_path)
            self.save_image_from_url(self.smallHeadImgUrl, save_path)
            print('保存头像', save_path)


class Contact(Person):
    def __init__(self, contact_info: Dict):
        super().__init__()
        self.wxid = contact_info.get('UserName')
        self.remark = contact_info.get('Remark')
        # Alias,Type,Remark,NickName,PYInitial,RemarkPYInitial,ContactHeadImgUrl.smallHeadImgUrl,ContactHeadImgUrl,bigHeadImgUrl
        self.alias = contact_info.get('Alias')
        self.nickName = contact_info.get('NickName')
        if not self.remark:
            self.remark = self.nickName
        self.remark = re.sub(r'[\\/:*?"<>|\s\.]', '_', self.remark)
        self.smallHeadImgUrl = contact_info.get('smallHeadImgUrl')
        self.smallHeadImgBLOG = b''
        self.avatar = None
        self.avatar_path = ""
        self.is_chatroom = self.wxid.__contains__('@chatroom')
        self.detail: Dict = contact_info.get('detail')
        self.label_name = contact_info.get('label_name')  # 联系人的标签分类

        """
        detail存储了联系人的详细信息，是个字典
        {
            'region': tuple[国家,省份,市], # 地区三元组
            'signature': str, # 个性签名
            'telephone': str, # 电话号码，自己写的备注才会显示
            'gender': int, # 性别 0：未知，1：男，2：女
        }
        """

    def save_avatar(self, path=None):
        if path:
            save_path = path
            if os.path.exists(save_path):
                self.avatar_path = save_path
                return save_path
        else:
            os.makedirs(f'{GlobalConfigs().path_data_dir}/avatar', exist_ok=True)
            save_path = os.path.join(GlobalConfigs().path_data_dir, 'avatar', self.wxid + '.png')
        self.avatar_path = save_path
        if not os.path.exists(save_path):
            # self.avatar.save(save_path)
            self.save_image_from_url(self.smallHeadImgUrl, save_path)
            print('保存头像', save_path)

    def get_uniquid_name(self):
        return f"{self.remark}({self.wxid})"


class ContactDefault(Person):
    def __init__(self, wxid=""):
        super().__init__()
        self.avatar = None
        self.avatar_path = ':/icons/icons/default_avatar.svg'
        self.wxid = wxid
        self.remark = wxid
        self.alias = wxid
        self.nickName = wxid
        self.smallHeadImgUrl = ""
        self.smallHeadImgBLOG = b''
        self.is_chatroom = False
        self.detail = {}


class Contacts:
    def __init__(self):
        self.contacts: Dict[str:Contact] = {}

    def add(self, wxid, contact: Contact):
        if wxid not in contact:
            self.contacts[wxid] = contact

    def get(self, wxid: str) -> Contact:
        return self.contacts.get(wxid)

    def remove(self, wxid: str):
        return self.contacts.pop(wxid)

    def save_avatar(self):
        avatar_dir = os.path.join(GlobalConfigs().path_data_dir, "avatar")
        for wxid, contact in self.contacts.items():
            avatar_path = os.path.join(avatar_dir, wxid + '.png')
            if os.path.exists(avatar_path):
                continue
            contact.save_avatar(avatar_path)


if __name__ == '__main__':
    p1 = Me()
    p2 = Me()
    print(p1 == p2)
