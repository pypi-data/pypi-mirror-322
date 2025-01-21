from PySide6 import QtCore
from beijing_fushengji.app.tools import load
from beijing_fushengji.widgets.styled_widget import StyledDialog


class PayDebt(StyledDialog):
    sig_pay = QtCore.Signal(int, int)

    def __init__(self, cash: int = 0, debt: int = 0):
        super().__init__()
        self.ui = load("ui.pay_debt").Ui_PayDebt()
        self.ui.setupUi(self)

        self.cash = cash
        self.debt = debt

        self.ui.spinBox.setMinimum(0)
        self.ui.spinBox.setMaximum(self.debt)
        if self.cash > self.debt:
            self.ui.spinBox.setValue(self.debt)
        else:
            self.ui.spinBox.setValue(self.cash)

        self.ui.pushButton.clicked.connect(self.pay)

        self.ui.label.setText(
            self.tr(
                'The village chief said on the phone: "Tie Niu, you owe me {} yuan, pay me back!"'
            ).format(self.debt)
        )

    def pay(self):
        pay_amount = self.ui.spinBox.value()
        self.cash -= pay_amount
        self.debt -= pay_amount
        self.sig_pay.emit(self.cash, self.debt)
        self.close()
