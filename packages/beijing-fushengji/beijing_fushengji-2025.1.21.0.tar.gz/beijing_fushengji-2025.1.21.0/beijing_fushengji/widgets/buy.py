from beijing_fushengji.app.models import Item, get_item_name
from beijing_fushengji.app.tools import load
from beijing_fushengji.widgets.styled_widget import StyledWidget


class Buy(StyledWidget):
    def __init__(self, cash: int, item: Item, current_store: int, max_store: int):
        super().__init__()
        self.cash = cash
        self.item = item

        self.ui = load("ui.buy").Ui_Buy()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)

        is_full = current_store == max_store
        if not is_full:
            max_count = self.cash // self.item.price
            avail_store = max_store - current_store

            if max_count > avail_store:
                max_count = avail_store
            self.ui.spinBox.setMinimum(1)
            self.ui.spinBox.setMaximum(max_count)
            self.ui.spinBox.setValue(max_count)

            self.ui.label.setText(
                self.tr(
                    "Your cash is RMB {}, which can be used to buy up to {} {}."
                ).format(self.cash, max_count, get_item_name(item))
            )
        else:
            self.ui.spinBox.setValue(0)
            self.ui.spinBox.setMinimum(0)
            self.ui.spinBox.setMaximum(0)
            self.ui.label.setText(
                self.tr(
                    "Your cash is RMB {}, the house you rented is full of stuff, so you can't get any more stock. \nTo expand your business, it is recommended that you rent a bigger house."
                ).format(self.cash)
            )
