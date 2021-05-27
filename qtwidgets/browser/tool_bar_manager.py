from PyQt5.QtWidgets import QSlider, QSpinBox, QPushButton


class ToolBarManager:
    def __init__(self, browser: 'BrowserWidget'):
        self.browser = browser

    def synchronize_toolbar(self):
        browser = self.browser
        config = browser.config

        self.page_selector.setValue(config.index)
        page_number = config.page_number(browser.model)
        self.page_selector.setRange(0, page_number - 1)
        if page_number <= 1:
            self.page_selector.hide()
        else:
            self.page_selector.show()

        self.item_per_line.setValue(config.item_per_line)
        self.item_per_page.setValue(config.item_per_page)
        browser.pageIndex.setText(f'{config.index + 1}/{page_number}')
        if config.tool_bar:
            browser.toolBar.show()
        else:
            browser.toolBar.hide()

    def setup_toolbar(self):
        browser = self.browser
        config = browser.config

        def on_item_per_line_change(value: int):
            config.item_per_line = value
            browser.request_update()

        def on_item_per_page_change(value: int):
            config.item_per_page = value
            browser.request_update()

        self.page_selector.valueChanged.connect(browser.select_page)
        self.item_per_page.valueChanged.connect(on_item_per_page_change)
        self.item_per_page.setValue(config.item_per_page)
        self.item_per_line.valueChanged.connect(on_item_per_line_change)
        self.item_per_line.setValue(config.item_per_line)
        self.clear_button.clicked.connect(lambda: browser.model.clear())

    @property
    def clear_button(self):
        widget: QPushButton = self.browser.clearButton
        return widget

    @property
    def page_selector(self):
        widget: QSlider = self.browser.pageSelector
        return widget

    @property
    def item_per_line(self):
        widget: QSpinBox = self.browser.itemPerLine
        return widget

    @property
    def item_per_page(self):
        widget: QSpinBox = self.browser.itemPerPage
        return widget
