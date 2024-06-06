from flet_core import *


class fletCommonUi:

    @staticmethod
    def show_snack_bar(page: Page, msg):
        page.snack_bar = SnackBar(
            behavior=SnackBarBehavior.FLOATING,
            # duration=200,
            content=Text(
                f"{msg}",
                size=14,
            )
        )
        page.snack_bar.open = True
        page.update()
