from pathlib import Path
from typing import Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLayout


def find_ui(name: str):
    # FIXME: https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
    path = Path(__file__).parent.parent / f'resources/ui/{name}.ui'
    return path


def load_ui(name: str, widget: QWidget):
    uic.loadUi(find_ui(name), widget)


def layout_iter(layout: QLayout, func: Callable[[QWidget], None]):
    if not layout:
        return
    items = [layout.itemAt(_) for _ in range(layout.count())]
    for item in items:
        w = item.widget()
        if w:
            func(w)

def layout_transfert(widget: QWidget, source: QLayout, target: QLayout):
    source.removeWidget(widget)
    target.addWidget(widget)
