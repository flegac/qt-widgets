from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


def find_ui(name: str):
    # FIXME: https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
    path = Path(__file__).parent.parent / f'resources/ui/{name}.ui'
    return path


def load_ui(name: str, widget: QWidget):
    uic.loadUi(find_ui(name), widget)
