from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation import report_view_model

__all__ = ("ReportView",)


class ReportView(qtw.QWidget):
    def __init__(
        self, *, report_name: str, view_model: report_view_model.ReportViewModel, height: int
    ):
        super().__init__()

        self.setMinimumHeight(height)

        self._report_name = report_name
        self._view_model = view_model

        self._table_view = qtw.QTableView()
        self._table_view.setSortingEnabled(True)
        self._table_view.setModel(self._view_model)

        bold_font = qtg.QFont()
        bold_font.setBold(True)

        title = qtw.QLabel()
        title.setFont(bold_font)
        title.setText(report_name)
        title.setMaximumWidth(200)

        self._last_refresh_label = qtw.QLabel()
        self._last_refresh_label.setFont(bold_font)
        self._last_refresh_label.setMaximumWidth(200)

        search_label = qtw.QLabel("Search")
        search_label.setFont(bold_font)
        search_label.setMaximumWidth(60)
        self._search_box = qtw.QLineEdit()
        self._search_box.setMaximumWidth(200)
        self._search_box.textChanged.connect(self._on_search_box_text_changed)

        self._refresh_button = qtw.QPushButton("Refresh")
        self._refresh_button.setFont(bold_font)
        self._refresh_button.setMaximumWidth(80)
        self._refresh_button.clicked.connect(self._on_refresh_button_clicked)

        header = qtw.QHBoxLayout()
        header.addWidget(title)
        header.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))
        header.addWidget(self._last_refresh_label)
        header.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))
        header.addWidget(search_label)
        header.addWidget(self._search_box)
        header.addWidget(self._refresh_button)

        layout = qtw.QVBoxLayout()
        layout.addLayout(header)
        layout.addWidget(self._table_view)
        self.setLayout(layout)

        self._view_model.modelReset.connect(self._table_view.resizeColumnsToContents)  # type: ignore

        self._view_model.last_refresh_updated.connect(self._update_last_refresh_label)

    def _on_refresh_button_clicked(self) -> None:
        self._view_model.refresh()

    def _on_search_box_text_changed(self, text: str) -> None:
        self._view_model.filter_text(text)

    def _update_last_refresh_label(self, dt_str: str) -> None:
        self._last_refresh_label.setText(dt_str)
