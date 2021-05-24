import sys

from PyQt5.QtWidgets import QApplication, QPushButton

from qtwidgets.browser.browser_config import BrowserConfig
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
            index=4,
            item_per_line=3,
            item_per_page=25,
        )
    )
    browser.set_model(model)
    sys.exit(app.exec_())
