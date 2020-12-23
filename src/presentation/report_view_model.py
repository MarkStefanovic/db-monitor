import datetime
import typing

from PyQt5 import QtCore as qtc

from src import domain, service

__all__ = ("ReportViewModel",)


class ReportViewModel(qtc.QAbstractTableModel):
    def __init__(self, /, signals: service.ReportWorkerSignals) -> None:
        super().__init__()

        self._signals = signals

        self._header: typing.List[str] = []
        self._data: typing.List[typing.Any] = []

        self._signals.result.connect(self.refresh)

    def columnCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._header)

    def data(self, index: qtc.QModelIndex, role: int = qtc.Qt.EditRole) -> typing.Any:
        if index.isValid() and role == qtc.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime.datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, datetime.date):
                return value.strftime("%Y-%m-%d")
            else:
                return value

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlags:
        return super().flags(index) | qtc.Qt.ItemIsEditable  # type: ignore

    @property
    def header(self) -> typing.List[str]:
        return self._header

    def headerData(
        self,
        section: int,
        orientation: qtc.Qt.Orientation,
        role: int = qtc.Qt.DisplayRole,
    ) -> typing.Any:
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._header[section]
        else:
            return super().headerData(section, orientation, role)

    def insertRows(
        self, row: int, count: int, parent: qtc.QModelIndex = qtc.QModelIndex()
    ) -> bool:
        self.beginInsertRows(parent or qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            default_row = [""] * len(self._header)
            self._data.insert(row, default_row)
        self.endInsertRows()
        return True

    def refresh(self, report: domain.Report) -> None:
        self.beginResetModel()
        self._header = report.header
        self._data = report.rows
        self.endResetModel()

    def removeRows(
        self, row: int, count: int, parent: qtc.QModelIndex = qtc.QModelIndex()
    ) -> bool:
        self.beginRemoveRows(parent or qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self._data[row]
        self.endRemoveRows()
        return True

    def rowCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._data)

    def setData(
        self, index: qtc.QModelIndex, value: typing.Any, role: int = qtc.Qt.EditRole
    ) -> bool:
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def sort(
        self, column: int, order: qtc.Qt.SortOrder = qtc.Qt.AscendingOrder
    ) -> None:
        self.layoutAboutToBeChanged.emit()  # type: ignore
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # type: ignore
