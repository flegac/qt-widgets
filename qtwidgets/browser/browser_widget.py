import math
from typing import List, Callable, Any, Generic, TypeVar

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.utils import load_ui, layout_transfert, layout_iter

WidgetBuilder = Callable[[Any], QWidget]

T = TypeVar('T')


class BrowserWidget(QWidget, Generic[T]):
    """
        TODO: configurable layout strategy (vertical vs horizontal first)
        TODO: use Generic[T] & typehint widget/data
    """

    def __init__(self, config: BrowserConfig, builder: WidgetBuilder, model: List[T] = None) -> None:
        super().__init__()
        self.config = config
        self.builder = builder
        self.model: List[T] = model or []

        self.widgets = dict()
        self._setup_ui()

    def is_empty(self):
        return len(self.model) == 0

    def add_item(self, item: T):
        self.model += [item]
        self._layout_update()

    def set_model(self, model: List[T]):
        self.model = model
        self._layout_update()

    def page_number(self):
        return math.ceil(len(self.model) / self.config.page.size)

    def select_page(self, index: int):
        if self.config.page.index == index:
            return
        self.config.page.index = index
        self._layout_update()

    def next_stack(self):
        stack: QStackedWidget = self.stackedWidget
        index = (stack.currentIndex() + 1) % stack.count()
        stack.setCurrentIndex(index)

    # building ui ----------------------------------------------------

    def _setup_ui(self):
        load_ui('browser', self)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._page.setLayout(layout)
        self._hidden.setLayout(QVBoxLayout())

        self._page_slider.valueChanged.connect(self.select_page)
        self._page_size_spinner.setValue(self.config.page.size)
        self._page_size_spinner.valueChanged.connect(self.on_page_size_change)
        self.show()

    def _layout_update(self):
        self._build_page(self.config.page.index)
        self._slider_update()
        self._label_update()

    def column_number(self, widgets: List[QWidget]):
        item_width = self.config.item.width
        if self.config.item.width is None:
            item_width = max([w.minimumWidth() for w in widgets])
            if item_width == 0:
                columns = math.floor(math.sqrt(len(widgets)))
                return columns

        safety_padding = self._scroll_area.verticalScrollBar().width()
        w = safety_padding + max(1, item_width)
        columns = max(1, math.floor(self.width() / w))
        return columns

    def _build_page(self, index: int):
        items = self.config.page.select(self.model, index)
        n = len(items)

        if n == 0:
            return

        widgets: List[QWidget] = [self._get_widget(item) for item in items]
        columns = self.column_number(widgets)

        old_layout: QGridLayout = self._page.layout()
        hidden_layout = self._hidden.layout()

        def hide_widget(w: QWidget):
            layout_transfert(w, old_layout, hidden_layout)

        layout_iter(old_layout, hide_widget)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        widget_width = math.floor(self.width()  / columns)

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

    def _slider_update(self):
        index = self.config.page.index
        page_number = self.page_number()

        self._page_slider.setValue(index)
        self._page_slider.setRange(0, page_number - 1)
        if page_number <= 1:
            self._page_slider.hide()
        else:
            self._page_slider.show()

    def _label_update(self):
        index = self.config.page.index
        page_number = self.page_number()

        visible = self.stackedWidget.currentWidget().layout().count()
        hidden = len(self.widgets) - self.stackedWidget.currentWidget().layout().count()
        label = f'page {index + 1}/{page_number} ({visible} visible widgets {hidden} hidden widgets)'
        self._page_label.setText(label)

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
    def _page_slider(self):
        slider: QSlider = self.pageSlider
        return slider

    @property
    def _page_label(self):
        label: QLabel = self.pageLabel
        return label

    @property
    def _page_size_spinner(self):
        size: QSpinBox = self.pageSize
        return size

    @property
    def _scroll_area(self):
        scroll: QScrollArea = self.scrollArea
        return scroll

    # custom events --------------------------------------------------

    def resizeEvent(self, event: QResizeEvent):
        self._layout_update()

    def on_page_size_change(self, value: int):
        self.config.page.size = value
        self._layout_update()
