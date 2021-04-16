from __future__ import annotations

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

        layout = qtw.QVBoxLayout()
        for i, report in enumerate(reports):
            if i % reports_per_row == 0:
                hbox = qtw.QHBoxLayout()
                layout.addLayout(hbox, stretch=1)

            vbox = qtw.QVBoxLayout()

            title = qtw.QLabel(report.report_name)
            title_font = qtg.QFont()
            title_font.setWeight(qtg.QFont.Bold)
            title.setFont(title_font)

            vbox.addWidget(title, alignment=qtc.Qt.AlignHCenter)
            vbox.addWidget(report)
            hbox.addLayout(vbox, stretch=1)  # noqa

            report.show()

        self.setLayout(layout)
