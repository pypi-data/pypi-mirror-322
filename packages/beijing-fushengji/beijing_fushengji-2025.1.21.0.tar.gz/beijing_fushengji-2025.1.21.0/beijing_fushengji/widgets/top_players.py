from PySide6 import QtWidgets, QtGui
from beijing_fushengji.ui.top_players import Ui_Form
from pathlib import Path
from beijing_fushengji.widgets.my_table_model import MyTableModel
from beijing_fushengji.widgets.styled_widget import StyledDialog


class TopPlayers(StyledDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = MyTableModel()
        self.ui.tableView.setModel(self.model)

        self.ui.tableView.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.tableView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.ui.ok.clicked.connect(self.close)

        self.init_data()
        self.show_scores()

    def show_scores(self):
        places_text = [
            self.tr("First place"),
            self.tr("Second place"),
            self.tr("Third place"),
            self.tr("Fourth place"),
            self.tr("Fifth place"),
            self.tr("Sixth place"),
            self.tr("Seventh place"),
            self.tr("Eighth place"),
            self.tr("Ninth place"),
            self.tr("Tenth place"),
        ]
        self.model.clear()

        self.model.setHorizontalHeaderLabels(
            [
                self.tr("Rank"),
                self.tr("Name"),
                self.tr("Money"),
                self.tr("Health"),
                self.tr("Reputation"),
            ]
        )
        for i in range(10):
            cell = QtGui.QStandardItem(str(places_text[i]))
            cells = [
                cell,
                *[
                    QtGui.QStandardItem(str(self.data[i][x]))
                    for x in range(len(self.data[0]))
                ],
            ]
            for cell in cells:
                cell.setFont(QtGui.QFont("MiSans", 12))
            self.model.appendRow(cells)

    def get_my_order(self, score):
        for i in range(len(self.data)):
            if score > self.data[i][1]:
                return i + 1
        return 100

    def insert_score(self, name, score, health, fame):
        fame = self.get_fame_str(fame)
        i = 0
        for x in self.data:
            if x[1] > score:
                i += 1
                continue
            else:
                break
        self.data.insert(i, [name, score, health, fame])
        self.save_score()
        self.show_scores()

    def init_data(self):
        self.model.setHorizontalHeaderLabels(
            [
                self.tr("Rank"),
                self.tr("Name"),
                self.tr("Money"),
                self.tr("Health"),
                self.tr("Reputation"),
            ]
        )

        header = self.ui.tableView.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
            )

        self.load_saved_score()

    def load_saved_score(self):
        score = Path(__file__).resolve().parent.parent.joinpath("score.txt")
        if not score.exists():
            self.data = [
                ["赖皮张", 12500720, 98, self.tr("controversial figure")],
                ["萧峰", 830050, 100, self.tr("outstanding youth")],
                ["二黑", 500447, 78, self.tr("highly respected")],
                ["Andy Rocky", 239403, 97, self.tr("very bad")],
                ["li xing", 34900, 35, self.tr("disdained by the world")],
                ["li xing", 13400, 100, self.tr("disdained by the world")],
                ["li", 2300, 77, self.tr("not good")],
                ["li", 45, 12, self.tr("outstanding youth")],
                ["li", 34, 100, self.tr("so-so")],
                ["li", 3, 100, self.tr("outstanding youth")],
            ]
            self.save_score()
        else:
            self.raw_data = score.read_text(encoding="utf8").split("\n")
            self.data = []
            i = 0
            loop_count = len(self.raw_data) // 4
            while i < loop_count * 4:
                row = []
                row.append(self.raw_data[i])
                row.append(int(self.raw_data[i + 1]))
                row.append(int(self.raw_data[i + 2]))
                row.append(self.raw_data[i + 3])

                i = i + 4
                self.data.append(row)

    def save_score(self):
        score = Path(__file__).resolve().parent.parent.joinpath("score.txt")
        score.write_text(
            "\n".join(["\n".join(map(str, i)) for i in self.data]), encoding="utf8"
        )

    def get_fame_str(self, fame):
        if fame >= 100:
            return self.tr("highly respected")
        elif fame < 100 and fame >= 90:
            return self.tr("outstanding youth")
        elif fame < 90 and fame >= 80:
            return self.tr("so-so")
        elif fame < 80 and fame >= 60:
            return self.tr("not good")
        elif fame < 60 and fame >= 40:
            return self.tr("controversial figure")
        elif fame < 40 and fame >= 20:
            return self.tr("bad")
        elif 10 <= fame < 20:
            return self.tr("very bad")
        elif fame < 10:
            return self.tr("disdained by the world")
        else:
            return self.tr("disdained by the world")
