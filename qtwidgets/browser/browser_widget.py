import math
from typing import List, Callable, Any, Generic, TypeVar

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.browser.page_layout import PageLayout
from qtwidgets.browser.tool_bar_manager import ToolBarManager
from qtwidgets.observablelist import observablelist
from qtwidgets.utils import load_ui, layout_transfert, layout_iter

WidgetBuilder = Callable[[Any], QWidget]
identity: WidgetBuilder = lambda x: x
T = TypeVar('T')


class BrowserWidget(QWidget, Generic[T]):
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

        self.toolbar_manager = ToolBarManager(self)
        self._setup_ui()

    def request_update(self):
        # new page building
        items = self.config.select(self.model, self.config.index)
        widgets = self.prepare_widgets(items, builder=self._get_widget)
        self._hide_current_page()
        layout = PageLayout(self.width(), widgets, self.config.item_per_line)
        self.change_current_page(layout)

        # other updates
        self.toolbar_manager.synchronize_toolbar()

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

    def select_page(self, index: int):
        if self.config.index == index:
            return
        self.config.index = index
        self.request_update()

    # building ui ----------------------------------------------------

    def _setup_ui(self):
        load_ui('browser', self)
        self.page_widget.setLayout(QGridLayout())
        self.hidden_widget.setLayout(QVBoxLayout())

        self.toolbar_manager.setup_toolbar()
        self.show()

    def _hide_current_page(self):
        old_layout: QGridLayout = self.page_widget.layout()
        hidden_layout = self.hidden_widget.layout()

        def hide_widget(w: QWidget):
            layout_transfert(w, old_layout, hidden_layout)

        layout_iter(old_layout, hide_widget)

    def prepare_widgets(self, items: List[T], builder: WidgetBuilder):
        hidden_layout = self.hidden_widget.layout()
        widgets: List[QWidget] = [builder(item) for item in items]
        for widget in widgets:
            hidden_layout.removeWidget(widget)
        return widgets

    def change_current_page(self, layout: PageLayout):
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

    # widget access ------------------------------------------------
    @property
    def hidden_widget(self):
        hidden: QWidget = self.hiddenWidget
        return hidden

    @property
    def page_widget(self):
        page: QWidget = self.pageWidget
        return page

    # custom events --------------------------------------------------
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.request_update()

    def _on_change(self, event):
        self.request_update()


def column_number(parent: BrowserWidget, widgets: List[QWidget], item_width: int = None):
    N = len(widgets)
    if N == 0:
        return 1

    width = parent.width()

    if item_width is None:
        item_width = max([w.minimumWidth() for w in widgets])
        if item_width == 0:
            columns = math.floor(math.sqrt(N))
            return columns

    safety_padding = parent.scrollArea.verticalScrollBar().width()
    w = safety_padding + max(1, item_width)
    columns = max(1, math.floor(width / w))
    return columns
