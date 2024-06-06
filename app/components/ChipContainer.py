from flet import *

from app.components.LocalImage import LocalImage


class ChipContainer(Container):
    def __init__(self, local_image_name, content: str, on_click=None, opacity: float = 1):
        super().__init__(on_click)
        self.content = Row(
            [LocalImage(local_image_name, width=20, height=20),
             Text(content, size=12, color=colors.BLACK, opacity=opacity)
             ],
            spacing=4
        )
        # self.width = 120
        self.height = 30
        self.opacity = opacity
        self.padding = padding.only(15, 3, 15, 3)
        self.border_radius = 5
        self.border = border.all(1, color=colors.BLACK12)
        self.ink = True
        self.expand = True
        self.ink_color = colors.BLUE_50
        self.on_click = on_click
        self.bgcolor = "#ebf6fd"
