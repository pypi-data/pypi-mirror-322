from PySide6 import QtWidgets

qss = """
    QLabel, QPushButton, QHeaderView, QStandardItem,
    QTextBrowser, QGroupBox, QTextEdit, QRadioButton, QCheckBox, 
    QAction, QMenu, QHeaderView {
        font: 12pt MiSans;
    }
    """



class StyledWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qss)


class StyledDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qss)
