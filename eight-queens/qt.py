import sys

try:
    from PyQt6 import QtGui, QtWidgets, QtCore
    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
except ImportError:
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtCore import Signal, Slot

#if 'PyQt6' in sys.modules:
#   # PyQt6
#    from PyQt6 import QtGui, QtWidgets, QtCore
#    from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
#
#
#else:
#    # PySide6
#    from PySide6 import QtGui, QtWidgets, QtCore
#    from PySide6.QtCore import Signal, Slot


def _enum(obj, name):
    parent, child = name.split('.')
    result = getattr(obj, child, False)
    if result:  # Found using short name only.
        return result

    obj = getattr(obj, parent)  # Get parent, then child.
    return getattr(obj, child)


def _exec(obj):
    if hasattr(obj, 'exec'):
        return obj.exec()
    else:
        return obj.exec_()
