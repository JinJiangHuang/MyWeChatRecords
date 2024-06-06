from flet import *

from app import config


class LocalImage(Image):
    def __init__(
            self,
            local_image_name: str,
            width=30,
            height=30,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.src = config.get_local_image_file_path(local_image_name)


class HomeNailLocalImage(LocalImage):
    def __init__(self, local_image_name: str, ):
        super().__init__(
            local_image_name, 30, 30
        )


class MenuLocalImage(LocalImage):
    def __init__(self, local_image_name: str, ):
        super().__init__(
            local_image_name, 20, 20
        )


class IconLocalImage(LocalImage):
    def __init__(self, local_image_name: str, ):
        super().__init__(
            local_image_name, 15, 15
        )
