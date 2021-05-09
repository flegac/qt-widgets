import math
import uuid
from typing import List, Callable, Any, Generic, TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from qtwidgets.flow.flow_config import FlowConfig
from qtwidgets.utils import load_ui, layout_transfert, layout_iter

WidgetBuilder = Callable[[Any], QWidget]

T = TypeVar('T')


class FlowWidget(QWidget, Generic[T]):
    """
        TODO: configurable layout strategy (vertical vs horizontal first)
        TODO: use Generic[T] & typehint widget/data
        TODO: do not rebuild widgets (use cache)
    """

    def __init__(self, config: FlowConfig, builder: WidgetBuilder, model: List[T] = None) -> None:
        super().__init__()
        self.config = config
        self.builder = builder
        self.model: List[T] = model or []

        self.widgets = dict()
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

    def next_stack(self):
        stack: QStackedWidget = self.stackedWidget
        index = (stack.currentIndex() + 1) % stack.count()
        stack.setCurrentIndex(index)

    # building ui ----------------------------------------------------

    def _setup_ui(self):
        load_ui('flow', self)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._page.setLayout(layout)
        self._hidden.setLayout(QVBoxLayout())

        self._page_slider.valueChanged.connect(self.select_page)
        self.nextStackButton.clicked.connect(self.next_stack)
        self.show()

    def _layout_update(self):
        self._build_page(self.config.page.index)
        self._slider_update()
        self._label_update()

    def _build_page(self, index: int):
        items = self.config.page.select(self.model, index)
        n = len(items)

        if n == 0:
            return

        widgets = [self._get_widget(item) for item in items]

        item_width = max([w.minimumWidth() for w in widgets])
        if self.config.item.width is not None:
            item_width = self.config.item.width
        if item_width == 0:
            item_width = min([w.width() for w in widgets])
        w = max(1, item_width)
        columns = max(1, math.floor(self.width() / w))

        old_layout: QGridLayout = self._page.layout()
        hidden_layout = self._hidden.layout()

        def hide_widget(w: QWidget):
            layout_transfert(w, old_layout, hidden_layout)

        layout_iter(old_layout, hide_widget)

        layout = QGridLayout()
        page = QWidget()
        page.setLayout(layout)

        for i in range(0, n, columns):
            for j, widget in enumerate(widgets[i:i + columns]):
                hidden_layout.removeWidget(widget)
                layout.addWidget(widget, i, j, Qt.AlignCenter)

        stack: QStackedWidget = self.stackedWidget
        stack.removeWidget(stack.currentWidget())
        stack.addWidget(page)
        stack.setCurrentWidget(page)

    def _get_widget(self, item: T):
        if not hasattr(item, '_uid'):
            item._uid = str(uuid.uuid4())
        if item._uid not in self.widgets:
            self.widgets[item._uid] = self.builder(item)
        return self.widgets[item._uid]

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
    def _scroll_area(self):
        scroll: QScrollArea = self.scrollArea
        return scroll

    # custom events --------------------------------------------------

    def resizeEvent(self, event: QResizeEvent):
        self._layout_update()
