import random
import sys
import time
from logging import Logger

from PyQt5.QtWidgets import QApplication

from qtwidgets.observablelist import observablelist
from qtwidgets.worker.worker import Task, Worker
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget


def create_worker():
    def task(i: int) -> Task:
        if i % 4 == 1:
            def work(logger: Logger):
                logger.debug('test logger')
                time.sleep(random.randint(500, 1000) / 1000)
                raise ValueError(i)

            return work

        def work(logger: Logger):
            logger.info('test logger -----------')

            time.sleep(random.randint(500, 1000) / 1000)
            res = f'work-{i}'
            return res

        return work

    return Worker((task(i) for i in range(10)))


if __name__ == '__main__':
    app = QApplication([])
    model = observablelist([create_worker() for i in range(1_000)])
    tasker = WorkerManagerWidget(model)
    sys.exit(app.exec())
