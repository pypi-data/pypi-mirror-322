from PySide6 import QtCore, QtWidgets, QtGui
from beijing_fushengji.app.models import get_item_name
from beijing_fushengji.widgets.my_table_model import MyTableModel


class BlackMarketTable(QtCore.QObject):
    def __init__(self, table: QtWidgets.QTableWidget):
        super().__init__()
        self.table = table

        font = QtGui.QFont("MiSans", 12)
        self.table.setFont(font)

        self.model_market = MyTableModel()
        self.table.setModel(self.model_market)

        self.enable_help = False
        import os

        if os.environ.get("ENABLE_HELP"):
            self.enable_help = True

    def slot_items(self, items):
        self.market_items = items
        self.model_market.clear()

        for item in self.market_items:
            name = QtGui.QStandardItem(get_item_name(item))
            icon = QtGui.QIcon(":/res/item.ico")
            name.setIcon(icon)
            price = QtGui.QStandardItem(str(item.price))
            percent = int((item.price - item.average_price) / item.average_price * 100)
            average_price = QtGui.QStandardItem(
                f"{int(item.average_price)}({'+' if percent>0 else ''}{percent}%)"
            )
            if self.enable_help:
                self.model_market.appendRow([name, price, average_price])

            else:
                self.model_market.appendRow([name, price])

        if self.enable_help:
            self.model_market.setHorizontalHeaderLabels(
                [
                    self.tr("Goods"),
                    self.tr("Black Market prices"),
                    self.tr("average price"),
                ]
            )
        else:
            self.model_market.setHorizontalHeaderLabels(
                [self.tr("Goods"), self.tr("Black Market prices")]
            )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        if self.enable_help:
            header.setSectionResizeMode(
                2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
            )
        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )


class MyItemsTable(QtCore.QObject):
    def __init__(self, table: QtWidgets.QTableWidget):
        super().__init__()
        self.table = table

        self.model_myitem = MyTableModel()
        self.table.setModel(self.model_myitem)
        font = QtGui.QFont("MiSans", 12)
        self.table.setFont(font)

    def slot_items(self, items):
        self.my_items = items
        self.model_myitem.clear()
        for item in self.my_items:
            name = QtGui.QStandardItem(get_item_name(item))
            icon = QtGui.QIcon(":/res/item.ico")
            name.setIcon(icon)
            price = QtGui.QStandardItem(str(item.price))
            quantity = QtGui.QStandardItem(str(item.quantity))
            self.model_myitem.appendRow([name, price, quantity])

        self.model_myitem.setHorizontalHeaderLabels(
            [self.tr("Goods"), self.tr("Bought price"), self.tr("Quantity")]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
