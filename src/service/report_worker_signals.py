from PyQt5 import QtCore as qtc


__all__ = ("ReportWorkerSignals",)


class ReportWorkerSignals(qtc.QObject):
    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    running = qtc.pyqtSignal()
    result = qtc.pyqtSignal(object)
