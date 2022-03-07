import sys
import types
import typing

import qtmodern.styles
import qtmodern.windows
from loguru import logger
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src import adapter, presentation, service


def main() -> None:
    logger.info("Starting Db Monitor...")
    config = adapter.load(path=adapter.fs.get_config_path())

    app = qtw.QApplication(sys.argv)

    app_icon = qtg.QIcon(str((adapter.fs.get_icons_folder() / "app.png").resolve()))

    default_font = qtg.QFont()
    default_font.setPointSize(9)
    default_font.setStyleHint(qtg.QFont.SansSerif)
    app.setFont(default_font)
    app.setWindowIcon(app_icon)

    ds_by_name = {ds.name: ds for ds in config.datasources}
    reports: typing.List[presentation.ReportView] = []

    thread_pool = qtc.QThreadPool()
    thread_pool.setMaxThreadCount(3)

    for job in config.jobs:
        signals = service.ReportWorkerSignals()
        ds = ds_by_name[job.datasource_name]
        view_model = presentation.ReportViewModel(signals)
        report = presentation.ReportView(
            report_name=job.report_name,
            view_model=view_model,
            height=job.height,
        )
        reports.append(report)
        service.ReportScheduler(
            thread_pool=thread_pool,
            ds=ds,
            job=job,
            signals=signals,
            parent=report,
            sql_folder=adapter.fs.get_sql_folder(),
        )

    window = presentation.MainView(
        reports=reports,
        reports_per_row=config.reports_per_row,
        app_icon=app_icon,
    )

    qtmodern.styles.dark(app)

    mw = qtmodern.windows.ModernWindow(window)
    mw.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    except_hook = sys.excepthook

    def exception_hook(
        exctype: typing.Type[BaseException],
        value: BaseException,
        traceback: types.TracebackType | None,
    ) -> None:
        logger.exception(value)
        except_hook(exctype, value, traceback)
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
    main()
