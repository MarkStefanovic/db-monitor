import datetime
import pathlib

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.dashboard import Dashboard
from src.presentation.report_view import ReportView

__all__ = ("MainView",)


class MainView(qtw.QMainWindow):
    def __init__(
        self,
        *,
        reports: list[ReportView],
        reports_per_row: int,
        app_icon: qtg.QIcon,
    ):
        super().__init__()

        self._dashboard = Dashboard(reports=reports, reports_per_row=reports_per_row)

        self._scroll_area = qtw.QScrollArea()
        self._scroll_area.setWidget(self._dashboard)

        self._scroll_area.setWidgetResizable(True)

        self.setWindowTitle("Db Monitor")
        self.setWindowIcon(app_icon)
        self.setWindowFlags(
            self.windowFlags()
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._dashboard)

        self.setStatusBar(qtw.QStatusBar())

        self.setCentralWidget(self._scroll_area)

        for report in reports:
            report.error.connect(self._on_error)

    def _on_error(self, error_message: str) -> None:
        self.statusBar().showMessage(f"{datetime.datetime.now():%I:%M:%S %p} [ERROR] {error_message}")
