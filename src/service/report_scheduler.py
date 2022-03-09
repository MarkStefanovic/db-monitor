import datetime
import typing

from loguru import logger
from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain

__all__ = ("ReportScheduler",)


class ReportScheduler(qtc.QObject):
    def __init__(
        self,
        *,
        thread_pool: qtc.QThreadPool,
        job: domain.Job,
        report_worker: domain.Worker,
        parent: qtw.QWidget,
    ) -> None:
        super().__init__(parent=parent)

        self._job = job
        self._report_worker = report_worker

        self._last_start_time: typing.Optional[datetime.datetime] = None

        self._thread_pool = thread_pool

        self._timer = qtc.QTimer()
        self._timer.timeout.connect(self._tick)  # noqa
        self._timer.start(1000)

    def _tick(self) -> None:
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
            self._run()

    def _run(self) -> None:
        logger.debug(f"Running {self._job.report_name} report...")
        # noinspection PyTypeChecker
        self._thread_pool.start(self._report_worker)
        self._last_start_time = datetime.datetime.now()
