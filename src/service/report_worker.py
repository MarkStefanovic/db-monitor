import functools
import pathlib

from PyQt5 import QtCore as qtc

import src.adapter.fs
from src import adapter, domain
from src.service import report_worker_signals

__all__ = ("ReportWorker",)


class ReportWorker(qtc.QRunnable):
    def __init__(
        self,
        *,
        ds: domain.Datasource,
        job: domain.Job,
        signals: report_worker_signals.ReportWorkerSignals,
        sql_folder: pathlib.Path,
    ):
        super().__init__()

        self._ds = ds
        self._job = job
        self._signals = signals
        self._sql_folder = sql_folder

        self._signals.refresh_request.connect(self.run)

    @functools.cached_property
    def sql(self) -> str:
        fp = self._sql_folder / self._job.sql_file
        return src.adapter.fs.read_sql_file(fp)

    def run(self) -> None:
        try:
            report = adapter.db.fetch(ds=self._ds, sql=self.sql)
            self._signals.result.emit(report)
        except Exception as e:
            self._signals.error.emit(f"An error occurred while refreshing {self._job.report_name}: {e!s}.")
        finally:
            self._signals.finished.emit()
