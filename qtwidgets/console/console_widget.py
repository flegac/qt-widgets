import logging
from copy import deepcopy
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QMenu

from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.utils import load_ui


class LogSignal(QObject):
    log = pyqtSignal(str)


class ConsoleWidget(QWidget):
    def __init__(self, config: ConsoleConfig):
        super().__init__()
        self.config = deepcopy(config)
        self.signals = LogSignal()
        self.signals.log.connect(self._write_line)
        self._setup_ui()
        self.handler = QtHandler(self.signals)
        self.set_loggers(config.loggers)

    def set_loggers(self, loggers: List[logging.Logger]):
        for logger in self.config.loggers:
            logger.removeHandler(self.handler)
        for logger in loggers:
            logger.addHandler(self.handler)
        self.config.loggers = loggers

    def clear(self):
        self._text_box.clear()

    def _write_line(self, log_text: str):
        self._text_box.appendPlainText(log_text)
        self._text_box.centerCursor()

    @property
    def _text_box(self) -> QPlainTextEdit:
        return self.textEdit

    def _setup_ui(self):
        load_ui('console', self)
        self._text_box.contextMenuEvent = self.contextMenuEvent
        self.show()

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu()
        clear = menu.addAction('clear')
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == clear:
            self.clear()


class QtHandler(logging.Handler):
    def __init__(self, signal: LogSignal):
        super().__init__()
        self.signal = signal
        self.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s'))
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        msg = self.format(record)
        self.signal.log.emit(msg)
