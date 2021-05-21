import random

import sys
from PyQt5.QtWidgets import QApplication, QPushButton

from qtwidgets.browser.browser_config import BrowserConfig, Item, Page
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.observablelist import observablelist

if __name__ == '__main__':
    # abstract model
    model = observablelist([f'data {_}' for _ in range(10_000)])


    def widget_builder(item: str):
        widget = QPushButton(item)
        # widget.setFixedWidth(random.randint(60, 150))
        # widget.setFixedHeight(random.randint(20, 50))
        widget.clicked.connect(lambda ev: model.remove(item))
        return widget


    # use Browser widget
    app = QApplication([])
    browser = BrowserWidget(
        builder=widget_builder,
        config=BrowserConfig(
            item=Item(
                width=175,
            ),
            page=Page(
                index=4,
                size=25
            ),
        ),
        model=model
    )
    sys.exit(app.exec_())
