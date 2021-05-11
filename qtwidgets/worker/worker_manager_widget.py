from typing import List

from PyQt5.QtCore import QThreadPool

from qtwidgets.browser.browser_config import BrowserConfig, Item, Page
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.worker.worker import Worker
from qtwidgets.worker.worker_widget import WorkerWidget


class WorkerManagerWidget(BrowserWidget):
    def __init__(self, workers: List[Worker] = None, config: BrowserConfig = None):
        self.pool = QThreadPool()
        super().__init__(
            config or BrowserConfig(
                # item=Item(width=250),
                page=Page(size=1)
            ),
            builder=self._worker_builder,
            model=workers
        )

    def _worker_builder(self, worker: Worker):
        return WorkerWidget(self.pool, worker)

    def start(self, worker: Worker):
        self.set_model(self.model + [worker])
