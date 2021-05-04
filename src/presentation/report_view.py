from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation import report_view_model

__all__ = ("ReportView",)


class ReportView(qtw.QWidget):
    def __init__(
        self, *, report_name: str, view_model: report_view_model.ReportViewModel
    ):
        super().__init__()

        self._report_name = report_name
        self._view_model = view_model

        self._table_view = qtw.QTableView()
        self._table_view.setSortingEnabled(True)
        self._table_view.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self._table_view.setModel(self._view_model)

        bold_font = qtg.QFont()
        bold_font.setBold(True)

        title = qtw.QLabel()
        title.setFont(bold_font)
        title.setText(report_name)

        self._last_refresh_label = qtw.QLabel()
        self._last_refresh_label.setFont(bold_font)

        self._refresh_button = qtw.QPushButton("Refresh")
        self._refresh_button.setFont(bold_font)
        self._refresh_button.setMaximumWidth(80)
        self._refresh_button.clicked.connect(self._on_refresh_button_clicked)

        header = qtw.QHBoxLayout()
        header.addWidget(title)
        header.addWidget(self._last_refresh_label)
        header.addWidget(self._refresh_button)

        layout = qtw.QVBoxLayout()
        layout.addLayout(header)
        layout.addWidget(self._table_view)
        self.setLayout(layout)

        self._view_model.modelReset.connect(self._table_view.resizeColumnsToContents)  # type: ignore

        self._view_model.last_refresh_updated.connect(self._update_last_refresh_label)

    # @property
    # def report_name(self) -> str:
    #     return self._report_name

    def _on_refresh_button_clicked(self) -> None:
        self._view_model.refresh()

    def _update_last_refresh_label(self, dt_str: str) -> None:
        self._last_refresh_label.setText(dt_str)
