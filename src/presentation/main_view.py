import pathlib
import typing

import qdarkgraystyle
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.dashboard import Dashboard
from src.presentation.report_view import ReportView

__all__ = ("MainView",)


class MainView(qtw.QMainWindow):
    def __init__(self, *, reports: typing.List[ReportView], reports_per_row: int, app_icon_fp: pathlib.Path, ):
        super().__init__()

        self._dashboard = Dashboard(reports=reports, reports_per_row=reports_per_row)

        self._scroll_area = qtw.QScrollArea()
        self._scroll_area.setWidget(self._dashboard)

        self._scroll_area.setWidgetResizable(True)

        self.setWindowTitle("Db Monitor")
        self.setWindowIcon(qtg.QIcon(str(app_icon_fp)))
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._dashboard)

        self.setCentralWidget(self._scroll_area)
