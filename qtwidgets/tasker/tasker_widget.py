from typing import List

from PyQt5.QtCore import QThreadPool

from qtwidgets.flow.flow_config import FlowConfig, Item, Page
from qtwidgets.flow.flow_widget import FlowWidget
from qtwidgets.tasker.worker import Worker
from qtwidgets.tasker.worker_widget import WorkerWidget


class TaskerWidget(FlowWidget):
    def __init__(self, workers: List[Worker] = None, config: FlowConfig = None):
        self.pool = QThreadPool()
        super().__init__(
            config or FlowConfig(
                item=Item(width=250),
                page=Page(size=10)
            ),
            builder=self._worker_builder,
            model=workers
        )

    def _worker_builder(self, worker: Worker):
        return WorkerWidget(self.pool, worker)

    def start(self, worker: Worker):
        self.set_model(self.model + [worker])
