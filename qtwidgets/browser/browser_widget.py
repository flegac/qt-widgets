import math
from typing import List, Callable, Any, Generic, TypeVar

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.observablelist import observablelist
from qtwidgets.utils import load_ui, layout_transfert, layout_iter

WidgetBuilder = Callable[[Any], QWidget]

identity: WidgetBuilder = lambda x: x

T = TypeVar('T')


class BrowserWidget(QWidget, Generic[T]):
    """
        TODO: configurable layout strategy (vertical vs horizontal first)
        TODO: use Generic[T] & typehint widget/data
    """

    def __init__(self,
                 parent: QWidget = None,
                 builder: WidgetBuilder = identity,
                 config: BrowserConfig = None
                 ):
        super().__init__(parent)
        self.config = config or BrowserConfig()
        self.builder = builder
        self.widgets = dict()
        self.model = observablelist()
        self.model.add_after_change_obervers(self._on_change)
        self._setup_ui()

    def request_update(self):
        self._build_page(self.config.index)
        self._config_update()
        self._label_update()
        if self.config.tool_bar:
            self.toolBar.show()
        else:
            self.toolBar.hide()

    def is_empty(self):
        return len(self.model) == 0

    def set_config(self, config: BrowserConfig):
        self.config = config
        self.request_update()

    def set_model(self, model: List[T]):
        assert isinstance(model, observablelist)
        self.model = model
        self.model.add_after_change_obervers(self._on_change)
        self.request_update()

    def page_number(self):
        if not self.model:
            return 0
        return math.ceil(len(self.model) / self.config.item_per_page)

    def select_page(self, index: int):
        if self.config.index == index:
            return
        self.config.index = index
        self.request_update()

    # building ui ----------------------------------------------------

    def _setup_ui(self):
        load_ui('browser', self)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._page.setLayout(layout)
        self._hidden.setLayout(QVBoxLayout())

        self.page_selector.valueChanged.connect(self.select_page)

        self.item_per_page.valueChanged.connect(self.on_item_per_page_change)
        self.item_per_page.setValue(self.config.item_per_page)

        self.item_per_line.valueChanged.connect(self.on_item_per_line_change)
        self.item_per_line.setValue(self.config.item_per_line)

        self.clearButton.clicked.connect(lambda: self.model.clear())

        self.show()

    def column_number(self, widgets: List[QWidget]):
        N = len(widgets)
        if N == 0:
            return 1

        width = self.width()

        item_width = self.config.item.width
        if item_width is None:
            item_width = max([w.minimumWidth() for w in widgets])
            if item_width == 0:
                columns = math.floor(math.sqrt(N))
                return columns

        safety_padding = self.scroll_area.verticalScrollBar().width()
        w = safety_padding + max(1, item_width)
        columns = max(1, math.floor(width / w))
        return columns

    def _build_page(self, index: int):
        items = self.config.select(self.model, index)
        n = len(items)

        widgets: List[QWidget] = [self._get_widget(item) for item in items]
        columns = self.config.item_per_line
        # columns = self.column_number(widgets)

        old_layout: QGridLayout = self._page.layout()
        hidden_layout = self._hidden.layout()

        def hide_widget(w: QWidget):
            layout_transfert(w, old_layout, hidden_layout)

        layout_iter(old_layout, hide_widget)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        widget_width = math.floor(self.width() / columns)

        for i in range(0, n, columns):
            for j, widget in enumerate(widgets[i:i + columns]):
                hidden_layout.removeWidget(widget)
                layout.addWidget(widget, i, j)
                widget.setMaximumWidth(widget_width)

        page = QWidget()
        page.setLayout(layout)

        stack: QStackedWidget = self.stackedWidget
        stack.removeWidget(stack.currentWidget())
        stack.addWidget(page)
        stack.setCurrentWidget(page)

    def _get_widget(self, item: T):
        key = hash(item)
        if key not in self.widgets:
            self.widgets[key] = self.builder(item)
        return self.widgets[key]

    def _config_update(self):
        self.item_per_line.setValue(self.config.item_per_line)
        self.item_per_page.setValue(self.config.item_per_page)
        self.page_selector.setValue(self.config.index)
        page_number = self.page_number()
        self.page_selector.setRange(0, page_number - 1)
        if page_number <= 1:
            self.page_selector.hide()
        else:
            self.page_selector.show()

    def _label_update(self):
        index = self.config.index
        page_number = self.page_number()
        label = f'{index + 1}/{page_number}'
        self.pageIndex.setText(label)

    # widget access ------------------------------------------------
    @property
    def _hidden(self):
        hidden: QWidget = self.hiddenWidget
        return hidden

    @property
    def _page(self):
        page: QWidget = self.pageWidget
        return page

    @property
    def page_selector(self):
        widget: QSlider = self.pageSelector
        return widget

    @property
    def item_per_line(self):
        widget: QSpinBox = self.itemPerLine
        return widget

    @property
    def item_per_page(self):
        widget: QSpinBox = self.itemPerPage
        return widget

    @property
    def scroll_area(self):
        scroll: QScrollArea = self.scrollArea
        return scroll

    # custom events --------------------------------------------------
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.request_update()

    def on_item_per_line_change(self, value: int):
        self.config.item_per_line = value
        self.request_update()

    def on_item_per_page_change(self, value: int):
        self.config.item_per_page = value
        self.request_update()

    def _on_change(self, event):
        self.request_update()
