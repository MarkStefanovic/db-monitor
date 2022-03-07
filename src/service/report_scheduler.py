import datetime
import pathlib
import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.service import report_worker_signals, report_worker

__all__ = ("ReportScheduler",)


class ReportScheduler(qtc.QObject):
    def __init__(
        self,
        *,
        thread_pool: qtc.QThreadPool,
        ds: domain.Datasource,
        job: domain.Job,
        signals: report_worker_signals.ReportWorkerSignals,
        parent: qtw.QWidget,
        sql_folder: pathlib.Path,
    ) -> None:
        super().__init__(parent=parent)

        self._ds = ds
        self._job = job
        self._signals = signals
        self._sql_folder = sql_folder

        self._last_start_time: typing.Optional[datetime.datetime] = None

        self._thread_pool = thread_pool

        self._timer = qtc.QTimer()
        self._timer.timeout.connect(self.tick)  # noqa
        self._timer.start(1000)

        self._signals.refresh_request.connect(self.run)

    def tick(self) -> None:
        if self._last_start_time:
            seconds_since_last_refresh = int(
                (datetime.datetime.now() - self._last_start_time).total_seconds()
            )
            if seconds_since_last_refresh >= self._job.seconds_between_refreshes:
                run_report = True
            else:
                run_report = False
        else:
            run_report = True

        if run_report:
            self.run()

    def run(self) -> None:
        logger.debug(f"Running {self._job.report_name} report...")
        worker = report_worker.ReportWorker(
            ds=self._ds,
            job=self._job,
            signals=self._signals,
            sql_folder=self._sql_folder,
        )
        self._thread_pool.start(worker)
        self._last_start_time = datetime.datetime.now()
