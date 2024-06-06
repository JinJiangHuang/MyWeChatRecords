from flet import *


class ExportChoiceItem(Container):
    def __init__(self, content: str, visible: bool, on_check_change):
        super().__init__()
        self.width = 160
        self.height = 30
        self.on_check_change = on_check_change
        self.padding = padding.symmetric(vertical=5, horizontal=0)
        self.opacity = 1 if visible else 0.3
        #
        self.check_box = Checkbox(
            disabled=not visible, value=visible, active_color="#0046ff",
            height=14, width=14,
            border_side=BorderSide(width=0.5),
            on_change=lambda e: self.on_check_change(e))

        self.user_name = Text(content, size=14, color="#102057")
        self.content = Row(
            [
                self.check_box, Container(width=8), self.user_name, Container(expand=1)
            ], spacing=0
        )
        self.on_click = lambda e: (self.toggle_checkbox())

    def toggle_checkbox(self):
        if self.check_box.disabled:
            return
        self.check_box.value = not self.check_box.value
        self.update()
        self.notify_check_change()

    def notify_check_change(self):
        if self.check_box.disabled:
            return
        is_check = self.check_box.value
        self.on_check_change(is_check)

    def set_checked(self, is_check):
        if self.check_box.disabled:
            return
        self.check_box.value = is_check
        self.notify_check_change()
