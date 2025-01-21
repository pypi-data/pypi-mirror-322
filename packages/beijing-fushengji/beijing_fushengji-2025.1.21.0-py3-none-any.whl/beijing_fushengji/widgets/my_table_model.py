from PySide6 import QtCore, QtGui


class MyTableModel(QtGui.QStandardItemModel):
    def __init__(self):
        super().__init__()

    def flags(self, index):
        flags = super().flags(index)
        return flags & ~QtCore.Qt.ItemFlag.ItemIsEditable
