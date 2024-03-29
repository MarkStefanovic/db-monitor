import datetime
import decimal
import typing

from PyQt5 import QtCore as qtc

from src import domain, service

__all__ = ("ReportViewModel",)


class ReportViewModel(qtc.QAbstractTableModel):
    error = qtc.pyqtSignal(str)
    last_refresh_updated = qtc.pyqtSignal(str)

    def __init__(
        self,
        *,
        signals: service.ReportWorkerSignals,
        report_worker: domain.Worker,
    ) -> None:
        super().__init__()

        self._signals = signals
        self._report_worker = report_worker

        self._header: list[str] = []
        self.__data: list[typing.Any] = []
        self._filter_text: str = ""

        self._signals.failed.connect(self._on_error)
        self._signals.finished.connect(self.reset)

    def columnCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._header)

    @property
    def _data(self) -> list[typing.Any]:
        if self._filter_text:
            return [
                row
                for row in self.__data
                if any(self._filter_text in str(v) for v in row)
            ]
        return self.__data

    def data(self, index: qtc.QModelIndex, role: int = qtc.Qt.EditRole) -> typing.Any:
        if index.isValid() and role == qtc.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime.datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, datetime.date):
                return value.strftime("%Y-%m-%d")
            elif isinstance(value, int):
                return f"{value:,.0f}"
            elif isinstance(value, (decimal.Decimal, float)):
                return f"{value:,.2f}"
            else:
                return value

    def filter_text(self, /, text: str) -> None:
        self._filter_text = text

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlags:
        return super().flags(index) | qtc.Qt.ItemIsEditable  # noqa

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
            self.__data.insert(row, default_row)
        self.endInsertRows()
        return True

    def refresh(self) -> None:
        self._report_worker.run()

    def reset(self, report: domain.Report) -> None:
        self.beginResetModel()
        self._header = report.header
        self.__data = report.rows
        self.endResetModel()

        self.last_refresh_updated.emit(datetime.datetime.now().strftime("%m/%d @ %H:%M:%S"))  # noqa

    def removeRows(
        self, row: int, count: int, parent: qtc.QModelIndex = qtc.QModelIndex()
    ) -> bool:
        self.beginRemoveRows(parent or qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self.__data[row]
        self.endRemoveRows()
        return True

    def rowCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._data)

    def setData(
        self, index: qtc.QModelIndex, value: typing.Any, role: int = qtc.Qt.EditRole
    ) -> bool:
        if index.isValid() and role == qtc.Qt.EditRole:
            self.__data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])  # noqa
            return True
        else:
            return False

    def sort(
        self, column: int, order: qtc.Qt.SortOrder = qtc.Qt.AscendingOrder
    ) -> None:
        self.layoutAboutToBeChanged.emit()  # noqa

        default_value = ""
        data_type_converter = str
        for row in self.__data:
            if row[column] is not None:
                if isinstance(row[column], (datetime.date, datetime.datetime)):
                    default_value = datetime.datetime(1900, 1, 1)
                    data_type_converter = lambda v: v  # noqa
                elif isinstance(row[column], (float, int)):
                    default_value = 0
                    data_type_converter = lambda v: v  # noqa
                break

        self.__data.sort(
            key=lambda r: default_value if r[column] is None else data_type_converter(r[column]),
            reverse=order == qtc.Qt.DescendingOrder,
        )

        self.layoutChanged.emit()  # noqa

    def _on_error(self, error_message: str) -> None:
        self.error.emit(error_message)  # noqa
