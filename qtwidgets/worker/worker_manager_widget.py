from PyQt5.QtCore import QThreadPool

from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.observablelist import observablelist
from qtwidgets.worker.worker import Worker
from qtwidgets.worker.worker_widget import WorkerWidget


class WorkerManagerWidget(BrowserWidget):
    def __init__(self, model: observablelist = None, config: BrowserConfig = None):
        self.pool = QThreadPool()
        super().__init__(
            model=model,
            config=config or BrowserConfig(
                # item=Item(width=250),
                page=Page(size=9)
            ),
            builder=self._worker_builder,
        )

    def _worker_builder(self, worker: Worker):
        widget = WorkerWidget(self.pool, worker)
        widget.abortButton.clicked.connect(lambda: self.model.remove(worker))
        return widget

    def start(self, worker: Worker):
        self.set_model(self.model + [worker])
