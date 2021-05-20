from PyQt5 import QtWidgets, QtCore


class DockWidget(QtWidgets.QDockWidget):
    # copied from : https://stackoverflow.com/questions/63638969/pyqt5-move-qdockwidget-by-dragging-tab
    def __init__(self, title: str):
        super().__init__(title)
        # self.setTitleBarWidget(QtWidgets.QWidget())
        self.dockLocationChanged.connect(self.on_dockLocationChanged)

    def on_dockLocationChanged(self):
        main: QtWidgets.QMainWindow = self.parent()
        all_dock_widgets = main.findChildren(QtWidgets.QDockWidget)

        for dock_widget in all_dock_widgets:
            sibling_tabs = main.tabifiedDockWidgets(dock_widget)
            # If you pull a tab out of a group the other tabs still see it as a sibling while dragging...
            sibling_tabs = [s for s in sibling_tabs if not s.isFloating()]

            if len(sibling_tabs) != 0:
                # Hide title bar
                dock_widget.setTitleBarWidget(QtWidgets.QWidget())
            else:
                # Re-enable title bar
                dock_widget.setTitleBarWidget(None)

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(100, 100)
