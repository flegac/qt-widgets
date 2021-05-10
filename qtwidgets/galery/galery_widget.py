from typing import List, Callable

import numpy as np
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap, QImage, QIcon, QResizeEvent
from PyQt5.QtWidgets import QPushButton

from qtwidgets.flow.flow_config import FlowConfig, Page
from qtwidgets.flow.flow_widget import FlowWidget, QSizePolicy
from qtwidgets.worker.worker import Worker
from qtwidgets.worker.worker_widget import WorkerWidget

Buffer = np.ndarray

RasterSource = Callable[[], Buffer]


def raster_builder():
    def builder(source: RasterSource):
        buffer = source()
        button = ImageButton(buffer)
        button.clicked.connect(print)
        return button

    return builder


class GaleryWidget(FlowWidget):
    def __init__(self, images: List[RasterSource] = None, config: FlowConfig = None):
        config = config or FlowConfig(
            page=Page(size=50)
        )
        self.pool = QThreadPool()
        super().__init__(
            config,
            builder=raster_builder(),
            model=images
        )

    def _worker_builder(self, worker: Worker):
        return WorkerWidget(self.pool, worker)

    def start(self, worker: Worker):
        self.set_model(self.model + [worker])


def pixmap_from_numpy(buffer: Buffer) -> QPixmap:
    buffer = buffer
    h, w = buffer.shape[:2]
    img = QImage(buffer.tobytes(), w, h, QImage.Format_RGB888)
    return QPixmap.fromImage(img)


class ImageButton(QPushButton):
    def __init__(self, buffer: Buffer):
        super().__init__()
        # self.setFlat(True)
        # self.setAutoFillBackground(True)

        self.setStyleSheet(f'QPushButton {{ color: rgb{0, 0, 0}; margin: 0px }}')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        h, w = buffer.shape[:2]
        self.buffer = buffer
        self.pixmap = pixmap_from_numpy(self.buffer)
        self.resize_pixmap(w, h)

    def resize_pixmap(self, w: int, h: int):
        self.icon = QIcon(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.setIcon(self.icon)
        size = QSize(w, h)
        self.setIconSize(size)

    def resizeEvent(self, ev: QResizeEvent) -> None:
        super().resizeEvent(ev)
        size = self.size()
        patch = 1
        dw=6+patch
        dh=4+patch
        self.resize_pixmap(size.width() - dw, size.height() - dh)
