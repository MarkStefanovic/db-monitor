import sys
import typing

from loguru import logger
from PyQt5 import QtGui as qtg, QtWidgets as qtw

from src import adapter, presentation, service

__all__ = ("run",)


@logger.catch
def run() -> None:
    logger.info("Starting Db Monitor...")
    config = adapter.load(adapter.fs.get_config_path())

    app = qtw.QApplication(sys.argv)

    default_font = qtg.QFont()
    default_font.setPointSize(9)
    default_font.setStyleHint(qtg.QFont.SansSerif)
    app.setFont(default_font)

    ds_by_name = {ds.name: ds for ds in config.datasources}
    reports: typing.List[presentation.ReportView] = []
    for job in config.jobs:
        signals = service.ReportWorkerSignals()
        ds = ds_by_name[job.datasource_name]
        view_model = presentation.ReportViewModel(signals)
        report = presentation.ReportView(report_name=job.report_name, view_model=view_model)
        reports.append(report)
        service.ReportScheduler(ds=ds, job=job, signals=signals, parent=report, sql_folder=adapter.fs.get_sql_folder())

    window = presentation.Dashboard(
        reports=reports, reports_per_row=config.reports_per_row, app_icon_fp=adapter.fs.get_icons_folder() / "app.png",
    )
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    if getattr(sys, "frozen", False):
        logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
    logger.add(
        adapter.fs.get_log_dir() / "info.log",
        rotation="5 MB",
        retention="7 days",
        level="INFO",
    )
    logger.add(
        adapter.fs.get_log_dir() / "error.log",
        rotation="5 MB",
        retention="7 days",
        level="ERROR",
    )
    run()
