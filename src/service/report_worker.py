import functools
import pathlib
import traceback

from PyQt5 import QtCore as qtc

import src.adapter.fs
from src import domain, adapter
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

    @functools.cached_property
    def sql(self) -> str:
        fp = self._sql_folder / self._job.sql_file
        return src.adapter.fs.read_sql_file(fp)

    def run(self):
        try:
            report = adapter.db.fetch(ds=self._ds, sql=self.sql)
            self._signals.result.emit(report)
        except Exception as e:
            traceback.print_exc()
            self._signals.error.emit((e, traceback.format_exc()))
        finally:
            self._signals.finished.emit()
