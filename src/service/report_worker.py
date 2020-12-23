import functools
import traceback

from PyQt5 import QtCore as qtc

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
    ):
        super().__init__()

        self._ds = ds
        self._job = job
        self._signals = signals

    @functools.cached_property
    def sql(self) -> str:
        return adapter.sql_file.read(self._job.sql_filepath)

    def run(self):
        try:
            report = adapter.db.fetch(ds=self._ds, sql=self.sql)
            self._signals.result.emit(report)
        except Exception as e:
            traceback.print_exc()
            self._signals.error.emit((e, traceback.format_exc()))
        finally:
            self._signals.finished.emit()
