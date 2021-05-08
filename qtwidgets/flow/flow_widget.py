import math
from typing import List, Callable, Any, Generic, TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from qtwidgets.flow.flow_config import FlowConfig
from qtwidgets.utils import load_ui

WidgetBuilder = Callable[[Any], QWidget]

T = TypeVar('T')


class FlowWidget(QWidget, Generic[T]):
    """
        TODO: configurable layout strategy (vertical vs horizontal first)
        TODO: use Generic[T] & typehint widget/data
    """

    def __init__(self, config: FlowConfig, builder: WidgetBuilder, model: List[T] = None) -> None:
        super().__init__()
        self.config = config
        self.builder = builder
        self.model: List[T] = model or []
        self._setup_ui()

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

    # widget access ------------------------------------------------
    @property
    def _page_slider(self):
        slider: QSlider = self.pageSlider
        return slider

    @property
    def _page_label(self):
        label: QLabel = self.pageLabel
        return label

    @property
    def _scroll_area(self):
        scroll: QScrollArea = self.scrollArea
        return scroll

    # custom events --------------------------------------------------

    def resizeEvent(self, event: QResizeEvent):
        self._layout_update()

    # building ui ----------------------------------------------------

    def _setup_ui(self):
        load_ui('flow', self)
        self._page_slider.valueChanged.connect(self.select_page)
        self.show()

    def _layout_update(self):
        self._slider_update()
        layout = self._build_page_layout(self.config.page.index)
        if layout:
            widget = QWidget()
            widget.setLayout(layout)
            self._scroll_area.setWidget(widget)

    def _build_page_layout(self, index: int):
        items = self.config.page.select(self.model, index)
        n = len(items)
        if n == 0:
            return None

        # prepare layout
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        widgets = [self.builder(item) for item in items]

        item_width = max([w.minimumWidth() for w in widgets])
        if self.config.item.width is not None:
            item_width = self.config.item.width
        if item_width == 0:
            item_width = min([w.width() for w in widgets])
        w = max(1, item_width)
        columns = max(1, math.floor(self.width() / w))

        for i in range(0, n, columns):
            for j, widget in enumerate(widgets[i:i + columns]):
                layout.addWidget(widget, i, j, Qt.AlignCenter)
        return layout

    def _slider_update(self):
        index = self.config.page.index
        page_number = self.page_number()

        # label
        self._page_label.setText(f'page {index + 1}/{page_number}')

        # slider
        self._page_slider.setValue(index)
        self._page_slider.setRange(0, page_number - 1)
        if page_number <= 1:
            self._page_slider.hide()
        else:
            self._page_slider.show()
