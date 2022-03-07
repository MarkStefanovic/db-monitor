from __future__ import annotations

import typing

from PyQt5 import QtGui as qtg, QtWidgets as qtw

from src.presentation import report_view

__all__ = ("Dashboard",)


class Dashboard(qtw.QWidget):
    def __init__(
        self,
        *,
        reports: typing.List[report_view.ReportView],
        reports_per_row: int,
    ):
        super().__init__()

        self._reports = reports
        self._reports_per_row = reports_per_row

        self._last_refresh_labels: typing.Dict[str, qtw.QLabel] = {}
        self._refresh_buttons: typing.Dict[str, qtw.QPushButton] = {}

        layout = qtw.QGridLayout()
        row_num = 0
        for i, report in enumerate(reports):
            col_num = i % reports_per_row
            if col_num == 0 and i > 0:
                row_num += 1
            bold_font = qtg.QFont()
            bold_font.setWeight(qtg.QFont.Bold)
            layout.addWidget(report, row_num, col_num)

        self.setLayout(layout)
