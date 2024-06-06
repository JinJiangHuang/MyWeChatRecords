from typing import Optional

from flet import *


def split_controls_array(arr, chunk_size):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]


class RowColumn(Column):
    def __init__(self, controls: Optional[list[Control]] = None, row_num: int = 2, padding=padding.symmetric(4, 0)):
        super().__init__()
        self.spacing = padding
        if not controls or row_num <= 0:
            return
        controls_list = split_controls_array(controls, row_num)
        for sub_controls in controls_list:
            sub_row = Row()
            for item_control in sub_controls:
                sub_row.controls.append(item_control)
            self.controls.append(sub_row)
