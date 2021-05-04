from __future__ import annotations

import datetime
import pathlib
import typing

import qdarkgraystyle
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation import report_view

__all__ = ("Dashboard",)


class Dashboard(qtw.QDialog):
    def __init__(
        self,
        *,
        reports: typing.List[report_view.ReportView],
        reports_per_row: int,
        app_icon_fp: pathlib.Path,
    ):
        super().__init__()

        self._reports = reports
        self._reports_per_row = reports_per_row

        self.setWindowTitle("Db Monitor")
        self.setWindowIcon(qtg.QIcon(str(app_icon_fp)))
        self.setGeometry(100, 100, 1200, 500)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        self._last_refresh_labels: typing.Dict[str, qtw.QLabel] = {}
        self._refresh_buttons: typing.Dict[str, qtw.QPushButton] = {}

        layout = qtw.QVBoxLayout()
        for i, report in enumerate(reports):
            if i % reports_per_row == 0:
                hbox = qtw.QHBoxLayout()
                layout.addLayout(hbox, stretch=1)

            bold_font = qtg.QFont()
            bold_font.setWeight(qtg.QFont.Bold)

            main_layout = qtw.QVBoxLayout()
            main_layout.addWidget(report)
            hbox.addLayout(main_layout, stretch=1)  # noqa

            report.show()

        self.setLayout(layout)
