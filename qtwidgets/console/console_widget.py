import logging
from copy import deepcopy
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QMenu, QComboBox

from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.observablelist import observablelist
from qtwidgets.utils import load_ui


class LogSignal(QObject):
    log = pyqtSignal(str)


class ConsoleWidget(QWidget):
    def __init__(self, config: ConsoleConfig = None):
        super().__init__()
        config = config or ConsoleConfig('console')

        self.records = observablelist()

        self.config = deepcopy(config)
        self.signals = LogSignal()
        self.signals.log.connect(self._write_line)
        self._setup_ui()
        self.handler = QtHandler(self.signals)
        self.set_loggers(config.loggers)

        combo: QComboBox = self.consoleLevel
        combo.currentIndexChanged.connect(self.change_level)

        self.consoleClearButton.clicked.connect(self.clear)

        self.consoleInput.returnPressed.connect(self.handle_input)

        self.context = dict()

    def handle_input(self):
        text = self.consoleInput.text()
        self.consoleInput.clear()
        self._write_line(f'> {text}')
        try:
            self.context = dict(self.context, **globals())
            exec(text, self.context, self.context)
        except Exception as e:
            self._write_line(str(e))

    def change_level(self, i):
        level = self.consoleLevel.currentText()
        print(level)
        self.clear()
        for record in self.records:
            if level in record:
                self._text_box.appendPlainText(record)

        self.handler.setLevel(level)

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
        self.records.append(log_text)

    @property
    def _text_box(self) -> QPlainTextEdit:
        return self.textEdit

    def _setup_ui(self):
        load_ui('console', self)
        self._text_box.contextMenuEvent = self.contextMenuEvent

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
