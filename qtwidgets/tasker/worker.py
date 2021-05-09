import logging
from dataclasses import dataclass
from typing import Callable, Any, List

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable

from qtwidgets.tasker.worker_status import WorkerStatus

Task = Callable[[logging.Logger], Any]


@dataclass
class Progress:
    done: int
    remaining: int

    @property
    def total(self):
        return self.done + self.remaining


class WorkerSignal(QObject):
    status = pyqtSignal(WorkerStatus)
    result = pyqtSignal(object)
    error = pyqtSignal(Exception)
    progress = pyqtSignal(Progress)


class Worker(QRunnable):
    def __init__(self, *tasks: List[Task]):
        super().__init__()
        self.signal = WorkerSignal()
        self.tasks = tasks
        self.logger = logging.getLogger(f'{self}')
        self.logger.setLevel(logging.DEBUG)
        self.canceled = False

    def run(self):
        try:
            self.canceled = False
            self.signal.status.emit(WorkerStatus.started)
            total = len(self.tasks)
            for i, task in enumerate(self.tasks):
                try:
                    if self.canceled:
                        break
                    res = task(self.logger)
                    self.signal.result.emit(res)
                except Exception as e:
                    self.signal.error.emit(e)
                self.signal.progress.emit(Progress(i + 1, total - i - 1))
        finally:
            self.signal.status.emit(WorkerStatus.finished)

    def abort(self):
        self.canceled = True
