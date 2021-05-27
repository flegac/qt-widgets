import math
from typing import List

from PyQt5.QtWidgets import QGridLayout, QWidget


class PageLayout(QGridLayout):

    def __init__(self, parent_width: int, widgets: List[QWidget], item_per_line: int):
        super(PageLayout, self).__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setup_ui(widgets, item_per_line, parent_width=parent_width)

    def setup_ui(self, widgets: List[QWidget], item_per_line: int, parent_width: int):
        n = len(widgets)
        if n == 0:
            return
        item_per_line = min(item_per_line, n)
        widget_width = math.floor((parent_width - 17) / item_per_line)
        for i in range(0, n, item_per_line):
            for j, widget in enumerate(widgets[i:i + item_per_line]):
                self.addWidget(widget, i, j)
                widget.setMaximumWidth(widget_width)
