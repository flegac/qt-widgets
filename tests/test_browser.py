import random
import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QPushButton

from qtwidgets.browser.browser_config import BrowserConfig, Item, Page
from qtwidgets.browser.browser_widget import BrowserWidget


def widget_builder(item: str):
    widget = QPushButton(item)
    widget.setFixedWidth(random.randint(60, 150))
    widget.setFixedHeight(random.randint(20, 50))
    return widget


if __name__ == '__main__':
    # abstract model
    model: List[str] = [f'data {_}' for _ in range(10_000)]

    # use Browser widget
    app = QApplication([])
    browser = BrowserWidget(
        config=BrowserConfig(
            item=Item(
                width=200,
            ),
            page=Page(
                index=4,
                size=25
            ),
        ),
        builder=widget_builder,
        model=model,
    )
    sys.exit(app.exec_())
