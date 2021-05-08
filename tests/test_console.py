import logging
import sys
import threading
import time

from PyQt5.QtWidgets import QApplication

from qtwidgets.console.console_widget import ConsoleWidget
from qtwidgets.console.console_config import ConsoleConfig


def start_logging_thread(name: str):
    log = logging.getLogger(name)

    def run():
        for i in range(20):
            log.debug(f'test')
            log.info(f'test')
            log.warning(f'test')
            log.error(f'test')
            time.sleep(0.2)

    thread = threading.Thread(target=run)
    thread.start()
    return log


if __name__ == '__main__':
    log1: logging.Logger = start_logging_thread('pif')
    log2: logging.Logger = start_logging_thread('paf')

    config = ConsoleConfig(
        name='log1',
        loggers=[log1, log2]
    )

    app = QApplication([])
    logs = ConsoleWidget(config)

    sys.exit(app.exec_())
