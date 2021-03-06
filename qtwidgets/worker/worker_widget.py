import logging

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget

from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.console.console_widget import ConsoleWidget
from qtwidgets.worker.worker import Worker
from qtwidgets.utils import load_ui

log = logging.getLogger()


class WorkerWidget(QWidget):
    def __init__(self, pool: QThreadPool, worker: Worker):
        super(WorkerWidget, self).__init__()
        self.pool = pool
        self.worker = worker
        self._setup_ui()
        self.is_running = False

    def _setup_ui(self):
        load_ui('worker', self)
        self.runButton.clicked.connect(self.run_task)
        self.abortButton.clicked.connect(self.abort_task)
        name = str(self.__class__.__name__)
        self.status.setText(f'{name}')

    def abort_task(self):
        self.worker.abort()

    def run_task(self):
        if self.is_running:
            log.error(f'Worker {self.worker} is already running')
            return
        self.is_running = True

        logs = ConsoleWidget(ConsoleConfig(
            'Worker',
            loggers=[self.worker.logger],
        ))
        self.layout().replaceWidget(self.logs, logs)
        self.worker.signal.status.connect(lambda status: self.status.setText(f'Status: {status}'))
        self.worker.signal.progress.connect(
            lambda progress: self.progress.setValue(int(100 * progress.done / progress.total)))
        self.worker.signal.error.connect(lambda e: self.error.setText(f'error: {e}'))
        self.worker.signal.result.connect(lambda e: self.result.setText(f'result: {e}'))
        self.pool.start(self.worker)
