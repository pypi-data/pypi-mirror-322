from beijing_fushengji.app.models import Status, Item, ItemName
from PySide6 import QtCore
import sys


class MainWindow(QtCore.QObject):
    def __init__(self):
        super().__init__()

    def print_items(self, items: list[Item]):
        if len(items) == 0:
            print(self.tr("No goods"))
        for item in items:
            print(self.tr("name"), end=":")
            if item.name == ItemName.car:
                print(self.tr("smuggled cars"))
            elif item.name == ItemName.cigar:
                print(self.tr("imported cigarettes"))
            elif item.name == ItemName.vcd_game:
                print(self.tr("Pirated VCDs and games"))
            elif item.name == ItemName.r18_book:
                print(self.tr("Shanghai baby (r18)"))
            elif item.name == ItemName.toys:
                print(self.tr("imported toys"))
            elif item.name == ItemName.makeup:
                print(self.tr("Fake cosmetics"))
            elif item.name == ItemName.liquor:
                print(self.tr("Fake liquor (highly toxic)"))
            elif item.name == ItemName.phone:
                print(self.tr("Counterfeit mobile phones"))
            print(self.tr("price"), ":", item.price)

    def print_market(self, items: list[Item]):
        print(self.tr("black market"))
        self.print_items(items)

    def print_my_items(self, items: list[Item]):
        print(self.tr("my items"))
        self.print_items(items)

    def print_status(self, status: Status):
        print(self.tr("cash"), status.cash)
        print(self.tr("saving"), status.saving)
        print(self.tr("debt"), status.debt)
        print(self.tr("health"), status.health)
        print(self.tr("fame"), status.fame)

    def makeDrugPrices(self, leaveout: int):
        self.goods = [ItemName(i) for i in range(8)]
        self.prices = [0 for i in range(8)]
        import random

        self.prices[0] = 100 + random.randint(0, 350)
        self.prices[1] = 15000 + random.randint(0, 15000)
        self.prices[2] = 5 + random.randint(0, 50)
        self.prices[3] = 1000 + random.randint(0, 2500)
        self.prices[4] = 5000 + random.randint(0, 9000)
        self.prices[5] = 250 + random.randint(0, 600)
        self.prices[6] = 750 + random.randint(0, 750)
        self.prices[7] = 65 + random.randint(0, 180)

        for _ in range(3):
            hide_item = random.randint(0, 7)
            self.prices[hide_item] = 0

        for i in range(8):
            if self.prices[i] != 0:
                item = Item()
                item.name = self.goods[i]
                item.price = self.prices[i]
                self.market_items.append(item)

    def start(self, status: Status, market_items: list[Item], my_items: list[Item]):
        self.status = status
        self.market_items = market_items
        self.my_items = my_items

        self.makeDrugPrices(3)

        while True:
            self.print_market(self.market_items)
            self.print_my_items(self.my_items)
            self.print_status(self.status)

            print(
                self.tr(
                    "Please choose: &Buy, &Sell, &Hospital, &Rent, &Net, &Post_office, Bank(k)"
                )
            )
            print(
                self.tr("Please choose: about_&beijing, &story, &doc, &intro, &about")
            )
            print(
                self.tr(
                    "Please choose: news(w), &tour_subway, tour_&city, switch_&mode"
                )
            )
            action = input(
                self.tr("Please choose: &new_game, &ranking, setting(t), &exit\n")
            )

            self.process_action(action)

    def process_action(self, action: str):
        if action == "e":
            sys.exit(0)


def main():
    app = QtCore.QCoreApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(":/translations/cn.qm")
    app.installTranslator(translator)
    window = MainWindow()
    window.start(Status(), [], [])
    sys.exit(app.exec())
