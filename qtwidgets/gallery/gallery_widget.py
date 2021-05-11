from typing import List, Callable

import numpy as np

from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton

RasterSource = Callable[[], np.ndarray]


class GalleryWidget(BrowserWidget):
    def __init__(self, config: BrowserConfig = None, model: List[RasterSource] = None):
        super().__init__(
            config=config or BrowserConfig(
                page=Page(size=50)
            ),
            builder=self.builder,
            model=model
        )

    def builder(self, source: RasterSource):
        buffer = source()
        button = ImageButton(buffer)
        return button
