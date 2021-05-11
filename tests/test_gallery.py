import random
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication

from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.gallery.gallery_widget import GalleryWidget


def source_factory():
    def source():
        width = 64
        aspect = .75 + random.random() * .5
        height = int(aspect * width)
        buffer = np.random.rand(height, width, 3)
        buffer *= 255
        buffer = buffer.astype('uint8')
        return buffer

    return source


if __name__ == '__main__':
    app = QApplication([])
    widget = GalleryWidget(
        images=[
            source_factory()
            for i in range(10_000)
        ],
        config=BrowserConfig(
            page=Page(size=20)
        )
    )

    sys.exit(app.exec())
