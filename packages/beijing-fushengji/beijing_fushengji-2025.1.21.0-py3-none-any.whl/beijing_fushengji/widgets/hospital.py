from PySide6 import QtCore
from beijing_fushengji.app.tools import load
from beijing_fushengji.widgets.styled_widget import StyledWidget


class Hospital(StyledWidget):
    sig_health = QtCore.Signal(int, int)

    def __init__(self, parent=None, cash: int = 0, health: int = 100):
        super().__init__()
        self.ui = load("ui.hospital").Ui_Hospital()
        self.ui.setupUi(self)

        self.cash = cash
        self.health = health
        self.cure_points = 100 - self.health
        self.needed_money = 3500 * self.cure_points

        self.ui.label_2.setText(
            self.tr(
                'The doctor clapped his hands happily: "Your health points are {}, and the points you need to be treated are {}.'
            ).format(self.health, self.cure_points)
        )
        self.ui.spinBox.setMinimum(0)
        self.ui.spinBox.setMaximum(self.cure_points)
        self.ui.spinBox.setValue(self.cure_points)

        self.ui.pushButton.clicked.connect(self.do_cure)

    def do_cure(self):
        self.needed_money = 3500 * self.ui.spinBox.value()
        if self.cash < self.needed_money:
            self.dialog = load("widgets.simple_dialogs").Diary()
            self.dialog.ui.label.setText(
                self.tr(
                    'The doctor said, "There\'s not enough money! I refuse to treat you."'
                )
            )
            self.dialog.exec()
        else:
            self.cash -= self.needed_money
            self.health += self.ui.spinBox.value()
            self.cure_points = 100 - self.health
            self.needed_money = 3500 * self.cure_points

            self.sig_health.emit(self.cash, self.health)
            self.close()
