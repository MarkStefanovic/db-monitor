from PyQt5 import QtCore as qtc

__all__ = ("ReportWorkerSignals",)


class ReportWorkerSignals(qtc.QObject):
    finished = qtc.pyqtSignal(object)
    failed = qtc.pyqtSignal(str)
    started = qtc.pyqtSignal()
