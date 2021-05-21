import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QSizePolicy, QToolButton
from qimage2ndarray import array2qimage


class ImageButton(QToolButton):
    def __init__(self, buffer: np.ndarray, name: str = None):
        super().__init__()
        # self.setAutoFillBackground(True)
        self.setStyleSheet(f'QToolButton {{ margin: 0px; }}')
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setText(name)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        h, w = buffer.shape[:2]
        self.aspect = w / h
        self.buffer = buffer
        self.pixmap = QPixmap.fromImage(array2qimage(self.buffer))
        self.resize_pixmap(h)

    def resize_pixmap(self, w: int):
        h = int(w / self.aspect)
        icon = QIcon(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.setIcon(icon)
        size = QSize(w, h)
        self.setIconSize(size)

    def resizeEvent(self, ev: QResizeEvent) -> None:
        super().resizeEvent(ev)
        size = self.size()
        patch = 1
        dw = 6 + patch
        width_dw = size.width() - dw
        self.resize_pixmap(width_dw)
