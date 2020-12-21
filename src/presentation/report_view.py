from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src.presentation import report_view_model

__all__ = ("ReportView",)


class ReportView(qtw.QTableView):
    def __init__(
        self, *, report_name: str, view_model: report_view_model.ReportViewModel
    ):
        super().__init__()

        self._report_name = report_name
        self._view_model = view_model

        self.setSortingEnabled(True)
        self.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self.setModel(self._view_model)

        self._view_model.modelReset.connect(self.resizeColumnsToContents)

    @property
    def report_name(self) -> str:
        return self._report_name
