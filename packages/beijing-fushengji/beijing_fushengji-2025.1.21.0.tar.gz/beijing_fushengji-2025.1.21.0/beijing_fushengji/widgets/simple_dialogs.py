from PySide6 import QtWidgets, QtCore
from beijing_fushengji.app.tools import load
import random

from beijing_fushengji.app.models import Item, get_item_name
from beijing_fushengji.widgets.styled_widget import StyledWidget
from beijing_fushengji.widgets.styled_widget import StyledDialog


class Airport(StyledWidget):
    def __init__(self):
        super().__init__()
        self.ui = load("ui.airport").Ui_Airport()
        self.ui.setupUi(self)


class BeijingIntro(StyledWidget):
    def __init__(self):
        super().__init__()
        self.ui = load("ui.beijing_intro").Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.close)


class CyberCafe(StyledDialog):
    def __init__(self):
        super().__init__()
        self.ui = load("ui.net_cafe").Ui_CyberCafe()
        self.ui.setupUi(self)
        self.show()

        self.ui.leave_cybercafe.clicked.connect(lambda _: self.close())


class Diary(StyledDialog):
    def __init__(self):
        super().__init__()

        self.ui = load("ui.diary").Ui_Diary()
        self.ui.setupUi(self)


class EasterEgg(StyledWidget):
    def __init__(self, detail=False):
        super().__init__()

        self.ui = load("ui.easteregg").Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)

        if not detail:
            self.ui.label.setText(
                self.tr(
                    "Author: Guo Xianghao, male, born in April 1970, graduated from Beijing University of Posts and Telecommunications in 1998 with a Ph.D. in artificial intelligence and natural language processing. Currently engaged in natural language processing research and software development. Loves games so much that he develops his own. Lived in Beijing for more than 10 years."
                )
            )
        else:
            self.ui.label.setText(
                self.tr(
                    "I love nature, art, and literature. I mainly use C/C++ for programming, but I am also very familiar with 80x86 assembly language. I once wrote a computer virus for my girlfriend (now the mother of my child). I am also proficient in LISP and Prolog languages, and have in-depth research on information retrieval technology and concept retrieval technology."
                )
            )


class News(StyledDialog):
    def __init__(self):
        super().__init__()
        self.ui = load("ui.news").Ui_News()
        self.ui.setupUi(self)


class Rent(StyledDialog):
    def __init__(self, money: int, max_quantity: int):
        super().__init__()
        self.ui = load("ui.rent").Ui_Rent()
        self.ui.setupUi(self)

        t = self.ui.label_2.text()
        t = t.format(max_quantity, int(money / 2), max_quantity + 10)
        self.ui.label_2.setText(t)

        self.ui.ok.clicked.connect(self.accept)
        self.ui.cancel.clicked.connect(self.reject)


class Sell(StyledWidget):
    def __init__(self, item: Item):
        super().__init__()
        self.item = item

        self.ui = load("ui.sell").Ui_Sell()
        self.ui.setupUi(self)
        self.item = item

        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setMaximum(item.quantity)
        self.ui.spinBox.setValue(item.quantity)

        self.ui.label.setText(
            self.tr("You have {} {}, how many do you want to sell?").format(
                item.quantity, get_item_name(item)
            )
        )
        self.ui.pushButton.clicked.connect(self.close)


class SendMoney(StyledWidget):
    def __init__(self):
        super().__init__()
        from beijing_fushengji.ui.send_money import Ui_SendMoney

        self.ui = Ui_SendMoney()
        self.ui.setupUi(self)


class Settings(StyledWidget):
    sig_settings = QtCore.Signal(bool, bool)

    def __init__(
        self, parent=None, allow_hacker: bool = False, turn_off_sound: bool = False
    ):
        super().__init__()
        from beijing_fushengji.ui.settings import Ui_Settings

        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.save_settings)
        self.ui.pushButton_2.clicked.connect(lambda: self.close())
        self.ui.allow_hacker.setChecked(allow_hacker)
        self.ui.turn_off_sound.setChecked(turn_off_sound)

    def save_settings(self):
        allow_hacker = self.ui.allow_hacker.isChecked()
        turn_off_sound = self.ui.turn_off_sound.isChecked()
        self.sig_settings.emit(allow_hacker, turn_off_sound)
        self.close()


class TextEditor(StyledWidget):
    def __init__(self):
        super().__init__()
        from beijing_fushengji.ui.text_editor import Ui_TextEditor

        self.ui = Ui_TextEditor()
        self.ui.setupUi(self)
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.ui.check_grammar.setFocus()
        self.ui.check_grammar.clicked.connect(self.check_grammar)

    def check_grammar(self):
        QtWidgets.QMessageBox.information(
            self,
            self.tr("Grammar"),
            self.tr(
                'Spell check suggestion: "Fragrant air" changed to "Fresh air"; "Boss" changed to "Boss lady".'
            ),
            QtWidgets.QMessageBox.StandardButton.Ok,
        )


class Statement(StyledWidget):
    def __init__(self):
        super().__init__()
        from beijing_fushengji.ui.statements import Ui_Statements

        self.ui = Ui_Statements()
        self.ui.setupUi(self)


class CelebrateWindow(StyledDialog):
    def __init__(self, score, order):
        super().__init__()

        self.ui = load("ui.celebrate").Ui_Form()
        self.ui.setupUi(self)

        self.messages = [
            self.tr("Outstanding money-maker in Beijing"),
            self.tr("Top 10 outstanding young people in Beijing"),
            self.tr("The coolest reseller in Beijing"),
            self.tr("The money-making master in Beijing"),
            self.tr("Beijing's No. 1 golden finger"),
        ]
        message = random.choice(self.messages)
        self.ui.l_summary.setText(self.ui.l_summary.text().format(score, order))
        self.ui.l_title.setText(self.ui.l_title.text().format(message))

        self.ui.pushButton.clicked.connect(self.check_name)

    def check_name(self):
        name = self.ui.lineEdit.text()
        if name.strip() == "":
            pass
        else:
            self.name = name
            self.close()

    def get_name(self):
        return self.name
