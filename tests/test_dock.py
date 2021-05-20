from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from qtwidgets.dock_widget import DockWidget


def build_dock(name: str, color: str):
    dock = DockWidget(name)
    dock.setAllowedAreas(Qt.AllDockWidgetAreas)
    content = QtWidgets.QWidget()
    content.setStyleSheet(f'background-color:{color};')
    content.setMinimumSize(QtCore.QSize(50, 50))
    dock.setWidget(content)
    return dock


# copied from : https://stackoverflow.com/questions/63638969/pyqt5-move-qdockwidget-by-dragging-tab

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = QtWidgets.QMainWindow()
    main.setDockOptions(main.GroupedDragging | main.AllowTabbedDocks | main.AllowNestedDocks)
    main.setTabPosition(Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)

    blues = [
        build_dock(f'Blue_{i}', 'blue')
        for i in range(4)
    ]
    greens = [
        build_dock(f'Green_{i}', 'green')
        for i in range(5)
    ]
    reds = [
        build_dock(f'Red_{i}', 'red')
        for i in range(3)
    ]
    main.addDockWidget(Qt.LeftDockWidgetArea, blues[0])
    for dock in blues[1:]:
        main.tabifyDockWidget(blues[0], dock)
    main.addDockWidget(Qt.LeftDockWidgetArea, greens[0])
    for dock in greens[1:]:
        main.tabifyDockWidget(greens[0], dock)

    main.addDockWidget(Qt.LeftDockWidgetArea, reds[0])
    for dock in reds[1:]:
        main.tabifyDockWidget(reds[0], dock)
    main.resize(400, 200)
    main.show()

    app.exec_()
