from flet import *


class BigButton(Container):
    def __init__(self, width=220, height=45, text_size=20, on_click=None):
        super().__init__()
        self.gradient = LinearGradient(
            begin=alignment.top_center,
            end=alignment.bottom_center,
            colors=[
                "0x3F84FF",
                "#0046FF",
            ],
            # tile_mode=GradientTileMode.MIRROR,
            # rotation=math.pi / 3,
        )
        self.ink = True
        self.on_click = on_click
        self.width = width
        self.height = height
        self.border_radius = 30
        self.alignment = alignment.center
        self.shadow = BoxShadow(spread_radius=3, color="#33aaaaaa")
        self.textview = Text("开始", color=colors.WHITE, weight=FontWeight.BOLD, size=text_size)
        self.content = self.textview

    def set_text(self, text):
        self.textview.value = text



