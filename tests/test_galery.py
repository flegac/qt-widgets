import random
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication

from qtwidgets.flow.flow_config import FlowConfig, Page
from qtwidgets.galery.galery_widget import GaleryWidget, Buffer


def source_factory():
    def source() -> Buffer:
        width = 64
        aspect = .5 + random.random() * 1.5
        height = int(aspect * width)
        buffer = np.random.rand(height, width, 3)
        buffer *= 255
        buffer = buffer.astype('uint8')
        return buffer

    return source


if __name__ == '__main__':
    app = QApplication([])
    widget = GaleryWidget(
        images=[
            source_factory()
            for i in range(1000)
        ],
        config=FlowConfig(
            page=Page(size=1)
        )
    )

    sys.exit(app.exec())
