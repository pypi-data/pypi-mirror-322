# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'story.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import beijing_fushengji.main_rc

class Ui_Story(object):
    def setupUi(self, Story):
        if not Story.objectName():
            Story.setObjectName(u"Story")
        Story.resize(586, 531)
        self.verticalLayout = QVBoxLayout(Story)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(Story)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(40, 0))
        self.widget.setMaximumSize(QSize(50, 16777215))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet(u"QWidget {\n"
"background-image: url(:/ICON/icon.ico);\n"
"background-repeat: none none;\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.widget)

        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addWidget(self.widget_2)

        self.label_2 = QLabel(Story)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(Story)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(Story)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.statusText = QLabel(Story)
        self.statusText.setObjectName(u"statusText")
        self.statusText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.statusText)

        self.startGame = QPushButton(Story)
        self.startGame.setObjectName(u"startGame")

        self.verticalLayout.addWidget(self.startGame)


        self.retranslateUi(Story)

        QMetaObject.connectSlotsByName(Story)
    # setupUi

    def retranslateUi(self, Story):
        Story.setWindowTitle(QCoreApplication.translate("Story", u"Beijing Life", None))
        self.label.setText(QCoreApplication.translate("Story", u"The story of \"Beijing Life\"", None))
        self.label_2.setText(QCoreApplication.translate("Story", u"You play the role of a young man who comes to Beijing from other places to make a living. At the beginning, you only have 2,000 yuan, and you still owe a debt of 5,500 yuan to the village chief (a gangster leader). The daily interest on these debts is as high as 10%. If you do not pay it off in time, the village chief will call fellow villagers in Beijing to beat you up, and you may die on the streets of Beijing. You decide to get rich by reselling various items on the black market at subway entrances across Beijing. Not only do you want to pay off your debts, but you also want to be ranked among the richest people in Beijing.", None))
        self.label_3.setText(QCoreApplication.translate("Story", u"You can only stay in Beijing for 40 days, and each visit to a black market counts as one day. In the beginning, you can only place 100 items in the house you rent. You will encounter various events in Beijing. You need to fight wits and courage with gangsters, thieves, murderers, corrupt officials, swindlers, etc. You also need to try to survive in Beijing's harsh natural environment.", None))
        self.label_4.setText(QCoreApplication.translate("Story", u"You will experience the excitement of selling pirated VCDs and smuggled cars in Beijing, as well as the funny events that are unique to our time.", None))
        self.statusText.setText(QCoreApplication.translate("Story", u"<status>", None))
        self.startGame.setText(QCoreApplication.translate("Story", u"Start Game >>", None))
    # retranslateUi

