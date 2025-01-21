from dataclasses import dataclass
from PySide6 import QtCore
from enum import Enum, auto
import random


@dataclass
class Status:
    cash: int = 2000
    saving: int = 0
    debt: int = 5000
    health: int = 100
    fame: int = 100


class ItemName(Enum):
    cigar = 0
    car = auto()
    vcd_game = auto()
    liquor = auto()
    r18_book = auto()
    toys = auto()
    makeup = auto()
    phone = auto()


@dataclass
class Item:
    name: ItemName = ItemName.car
    price: int = 0
    quantity: int = 0


def get_item_name(item: Item) -> str:
    if item.name == ItemName.cigar:
        return QtCore.QCoreApplication.translate("Item", "imported cigarettes")
    elif item.name == ItemName.car:
        return QtCore.QCoreApplication.translate("Item", "smuggled cars")
    elif item.name == ItemName.vcd_game:
        return QtCore.QCoreApplication.translate("Item", "Pirated VCDs and games")
    elif item.name == ItemName.liquor:
        return QtCore.QCoreApplication.translate("Item", "Fake liquor (highly toxic)")
    elif item.name == ItemName.r18_book:
        return QtCore.QCoreApplication.translate("Item", "Shanghai baby (r18)")
    elif item.name == ItemName.toys:
        return QtCore.QCoreApplication.translate("Item", "imported toys")
    elif item.name == ItemName.makeup:
        return QtCore.QCoreApplication.translate("Item", "Fake cosmetics")
    elif item.name == ItemName.phone:
        return QtCore.QCoreApplication.translate("Item", "Counterfeit mobile phones")


def makeDrugPrices(leaveout: int) -> list[Item]:
    market_items = []
    goods = [ItemName(i) for i in range(8)]
    prices = [0 for i in range(8)]

    prices[0] = 100 + random.randint(0, 350)
    prices[1] = 15000 + random.randint(0, 15000)
    prices[2] = 5 + random.randint(0, 50)
    prices[3] = 1000 + random.randint(0, 2500)
    prices[4] = 5000 + random.randint(0, 9000)
    prices[5] = 250 + random.randint(0, 600)
    prices[6] = 750 + random.randint(0, 750)
    prices[7] = 65 + random.randint(0, 180)

    average_prices = [0 for _ in range(8)]
    average_prices[0] = 100 + 350/2
    average_prices[1] = 15000 + 15000/2
    average_prices[2] = 5 + 50/2
    average_prices[3] = 1000 + 2500/2
    average_prices[4] = 5000 + 9000/2
    average_prices[5] = 250 + 600/2
    average_prices[6] = 750 + 750/2
    average_prices[7] = 65 + 180/2

    if leaveout != 0:
        hide_num = random.choices(
            population=[1, 2, 3], weights=[15372, 328392, 655876], k=1
        )[0]
        hide_items = random.sample(range(8), hide_num)
        for i in hide_items:
            prices[i] = 0

    for i in range(8):
        if prices[i] != 0:
            item = Item()
            item.name = goods[i]
            item.price = prices[i]
            item.average_price = average_prices[i]
            market_items.append(item)

    return market_items
