from typing import Callable

import numpy as np

from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton

RasterSource = Callable[[], np.ndarray]


class GalleryWidget(BrowserWidget):
    def __init__(self, config: BrowserConfig = None):
        super().__init__(builder=self.builder, config=config)

    def builder(self, source: RasterSource):
        buffer = source()
        button = ImageButton(buffer, name='test_label')
        return button
