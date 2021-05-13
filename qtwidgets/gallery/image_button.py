import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QResizeEvent, QPixmap, QImage
from PyQt5.QtWidgets import QPushButton, QSizePolicy


def pixmap_from_numpy(buffer: np.ndarray) -> QPixmap:
    buffer = buffer
    h, w = buffer.shape[:2]
    img = QImage(buffer.tobytes(), w, h, QImage.Format_RGB888)
    return QPixmap.fromImage(img)


class ImageButton(QPushButton):
    def __init__(self, buffer: np.ndarray):
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
        icon = QIcon(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.setIcon(icon)
        size = QSize(w, h)
        self.setIconSize(size)

    def resizeEvent(self, ev: QResizeEvent) -> None:
        super().resizeEvent(ev)
        size = self.size()
        patch = 1
        dw = 6 + patch
        dh = 4 + patch
        self.resize_pixmap(size.width() - dw, size.height() - dh)
