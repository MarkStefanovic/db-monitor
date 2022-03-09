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

        self.setAutoDelete(False)

        self._ds = ds
        self._job = job
        self._signals = signals

        fp: pathlib.Path = sql_folder / job.sql_file
        if not fp.exists():
            raise domain.exceptions.FileDoesNotExist(path=fp)

        self._sql = src.adapter.fs.read_sql_file(fp)

    def run(self) -> None:
        try:
            report = adapter.db.fetch(ds=self._ds, sql=self._sql)
            self._signals.finished.emit(report)
        except Exception as e:
            self._signals.failed.emit(f"An error occurred while refreshing {self._job.report_name}: {e!s}.")
