import random
import sys
import time
from logging import Logger

from PyQt5.QtWidgets import QApplication

from qtwidgets.tasker.tasker_widget import TaskerWidget
from qtwidgets.tasker.worker import Task, Worker


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

    return Worker(*[task(i) for i in range(10)])


if __name__ == '__main__':
    app = QApplication([])
    tasker = TaskerWidget([
        create_worker()
        for i in range(1000)
    ])

    sys.exit(app.exec())
