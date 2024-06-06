from flet import *

from app.components.LocalImage import LocalImage


class ChipBtn(Container):
    def __init__(self, local_image_name, content: str, on_click=None, opacity: float = 1.0):
        super().__init__(on_click)
        self.content = Row(
            [LocalImage(local_image_name, width=12, height=12),
             Text(content, size=11.5, color="#102057",  weight=FontWeight.BOLD, opacity=opacity)
             ],
            spacing=4
        )
        # self.width = 120
        self.height = 30
        self.opacity = opacity
        self.padding = padding.only(15, 3, 10, 3)
        self.border_radius = 5
        self.border = border.all(0.9, color="#0046FF")
        self.ink = True
        self.padding = padding.symmetric(2, 12)
        self.ink_color = colors.BLUE_50
        self.on_click = on_click
        self.bgcolor = "#f8faff"

