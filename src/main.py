import pathlib
import sys
import typing

from PyQt5 import QtWidgets as qtw
from loguru import logger

from src import adapter, presentation, service

__all__ = ("run",)


@logger.catch
def run(config_filepath: pathlib.Path) -> None:
    logger.info("Starting Db Monitor...")
    config = adapter.load(config_filepath)
    error_log_fp = config.log_dir / "error.log"
    logger.add(
        error_log_fp,
        rotation="5 MB",
        retention="7 days",
        level="ERROR",
    )
    logger.info(f"Logging errors to {error_log_fp!s}.")

    app = qtw.QApplication(sys.argv)

    ds_by_name = {ds.name: ds for ds in config.datasources}
    reports: typing.List[presentation.ReportView] = []
    for job in config.jobs:
        signals = service.ReportWorkerSignals()
        ds = ds_by_name[job.datasource_name]
        view_model = presentation.ReportViewModel(signals)
        report = presentation.ReportView(report_name=job.report_name, view_model=view_model)
        reports.append(report)
        service.ReportScheduler(ds=ds, job=job, signals=signals, parent=report)

    window = presentation.Dashboard(
        reports=reports, reports_per_row=config.reports_per_row
    )
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    config_fp = pathlib.Path(sys.argv[0]).parent.parent / "data" / "config.json"
    run(config_fp)
