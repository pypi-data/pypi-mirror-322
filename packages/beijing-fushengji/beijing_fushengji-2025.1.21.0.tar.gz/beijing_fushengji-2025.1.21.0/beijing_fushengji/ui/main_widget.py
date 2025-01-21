# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLCDNumber, QLabel, QPushButton,
    QSizePolicy, QTableView, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)
import beijing_fushengji.main_rc

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(943, 603)
        self.verticalLayout_7 = QVBoxLayout(MainWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget = QWidget(MainWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 0, 9, 0)

        self.verticalLayout_7.addWidget(self.widget)

        self.widget_14 = QWidget(MainWidget)
        self.widget_14.setObjectName(u"widget_14")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.widget_12 = QWidget(self.widget_14)
        self.widget_12.setObjectName(u"widget_12")
        self.verticalLayout_4 = QVBoxLayout(self.widget_12)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.widget_12)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.black_market = QTableView(self.widget_12)
        self.black_market.setObjectName(u"black_market")
        self.black_market.setStyleSheet(u"QHeaderView, QStandardItem {\n"
"                font: 12pt MiSans;\n"
"}")

        self.verticalLayout_4.addWidget(self.black_market)


        self.horizontalLayout_7.addWidget(self.widget_12)

        self.widget_8 = QWidget(self.widget_14)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(120, 200))
        self.widget_8.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_2 = QVBoxLayout(self.widget_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_8 = QLabel(self.widget_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_8)

        self.buy = QPushButton(self.widget_8)
        self.buy.setObjectName(u"buy")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buy.sizePolicy().hasHeightForWidth())
        self.buy.setSizePolicy(sizePolicy1)
        self.buy.setMaximumSize(QSize(16777215, 38))

        self.verticalLayout_2.addWidget(self.buy)

        self.label_9 = QLabel(self.widget_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_9)

        self.sell = QPushButton(self.widget_8)
        self.sell.setObjectName(u"sell")
        sizePolicy1.setHeightForWidth(self.sell.sizePolicy().hasHeightForWidth())
        self.sell.setSizePolicy(sizePolicy1)
        self.sell.setMaximumSize(QSize(16777215, 38))

        self.verticalLayout_2.addWidget(self.sell)


        self.horizontalLayout_7.addWidget(self.widget_8)

        self.widget_13 = QWidget(self.widget_14)
        self.widget_13.setObjectName(u"widget_13")
        self.verticalLayout_5 = QVBoxLayout(self.widget_13)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_7)

        self.my_room = QTableView(self.widget_13)
        self.my_room.setObjectName(u"my_room")
        self.my_room.setStyleSheet(u"QHeaderView, QStandardItem {\n"
"                font: 12pt MiSans;\n"
"}")

        self.verticalLayout_5.addWidget(self.my_room)


        self.horizontalLayout_7.addWidget(self.widget_13)


        self.verticalLayout_7.addWidget(self.widget_14)

        self.widget_15 = QWidget(MainWidget)
        self.widget_15.setObjectName(u"widget_15")
        self.widget_15.setStyleSheet(u"QPushButton::disabled{\n"
"	background-color: rgb(143, 240, 164);\n"
"        color: black;\n"
"}")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_15)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.groupBox = QGroupBox(self.widget_15)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.groupBox.setMinimumSize(QSize(250, 191))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(5, -1, 5, 5)
        self.widget_3 = QWidget(self.groupBox)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.cash = QLCDNumber(self.widget_4)
        self.cash.setObjectName(u"cash")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cash.sizePolicy().hasHeightForWidth())
        self.cash.setSizePolicy(sizePolicy3)
        self.cash.setStyleSheet(u"color: rgb(87, 227, 137);")
        self.cash.setDigitCount(8)

        self.horizontalLayout_2.addWidget(self.cash)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.saving = QLCDNumber(self.widget_5)
        self.saving.setObjectName(u"saving")
        sizePolicy3.setHeightForWidth(self.saving.sizePolicy().hasHeightForWidth())
        self.saving.setSizePolicy(sizePolicy3)
        self.saving.setStyleSheet(u"color: rgb(87, 227, 137);")
        self.saving.setDigitCount(8)

        self.horizontalLayout_4.addWidget(self.saving)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_6)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.debt = QLCDNumber(self.widget_6)
        self.debt.setObjectName(u"debt")
        sizePolicy3.setHeightForWidth(self.debt.sizePolicy().hasHeightForWidth())
        self.debt.setSizePolicy(sizePolicy3)
        self.debt.setStyleSheet(u"color: rgb(240, 0, 0);")
        self.debt.setSmallDecimalPoint(False)
        self.debt.setDigitCount(8)
        self.debt.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self.horizontalLayout_5.addWidget(self.debt)


        self.verticalLayout.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.widget_3)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.health = QLCDNumber(self.widget_7)
        self.health.setObjectName(u"health")
        sizePolicy3.setHeightForWidth(self.health.sizePolicy().hasHeightForWidth())
        self.health.setSizePolicy(sizePolicy3)
        self.health.setStyleSheet(u"color: rgb(87, 227, 137);")

        self.horizontalLayout_3.addWidget(self.health)

        self.label_6 = QLabel(self.widget_7)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.fame = QLCDNumber(self.widget_7)
        self.fame.setObjectName(u"fame")
        sizePolicy3.setHeightForWidth(self.fame.sizePolicy().hasHeightForWidth())
        self.fame.setSizePolicy(sizePolicy3)
        self.fame.setStyleSheet(u"color: rgb(87, 227, 137);")

        self.horizontalLayout_3.addWidget(self.fame)


        self.verticalLayout.addWidget(self.widget_7)


        self.gridLayout.addWidget(self.widget_3, 0, 0, 1, 1)


        self.horizontalLayout_8.addWidget(self.groupBox)

        self.widget_10 = QWidget(self.widget_15)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy4)
        self.widget_10.setMinimumSize(QSize(160, 190))
        self.widget_10.setMaximumSize(QSize(300, 190))
        self.verticalLayout_3 = QVBoxLayout(self.widget_10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.switch_place = QPushButton(self.widget_10)
        self.switch_place.setObjectName(u"switch_place")
        sizePolicy1.setHeightForWidth(self.switch_place.sizePolicy().hasHeightForWidth())
        self.switch_place.setSizePolicy(sizePolicy1)
        self.switch_place.setMinimumSize(QSize(0, 0))
        self.switch_place.setStyleSheet(u"QPushButton{\n"
"border: none;\n"
"}")

        self.verticalLayout_3.addWidget(self.switch_place)

        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_6 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 2)
        self.x1 = QPushButton(self.widget_11)
        self.x1.setObjectName(u"x1")
        sizePolicy1.setHeightForWidth(self.x1.sizePolicy().hasHeightForWidth())
        self.x1.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.x1)

        self.x2 = QPushButton(self.widget_11)
        self.x2.setObjectName(u"x2")
        sizePolicy1.setHeightForWidth(self.x2.sizePolicy().hasHeightForWidth())
        self.x2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.x2)


        self.verticalLayout_3.addWidget(self.widget_11)

        self.switch_mode = QPushButton(self.widget_10)
        self.switch_mode.setObjectName(u"switch_mode")
        sizePolicy1.setHeightForWidth(self.switch_mode.sizePolicy().hasHeightForWidth())
        self.switch_mode.setSizePolicy(sizePolicy1)
        self.switch_mode.setStyleSheet(u"QPushButton{\n"
"border: none;\n"
"}")

        self.verticalLayout_3.addWidget(self.switch_mode)


        self.horizontalLayout_8.addWidget(self.widget_10)

        self.widget_9 = QWidget(self.widget_15)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy4.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy4)
        self.widget_9.setMinimumSize(QSize(261, 191))
        self.gridLayout_2 = QGridLayout(self.widget_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.x8 = QPushButton(self.widget_9)
        self.x8.setObjectName(u"x8")
        sizePolicy1.setHeightForWidth(self.x8.sizePolicy().hasHeightForWidth())
        self.x8.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x8, 2, 0, 1, 1)

        self.x5 = QPushButton(self.widget_9)
        self.x5.setObjectName(u"x5")
        sizePolicy.setHeightForWidth(self.x5.sizePolicy().hasHeightForWidth())
        self.x5.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x5, 0, 2, 1, 1)

        self.x6 = QPushButton(self.widget_9)
        self.x6.setObjectName(u"x6")
        sizePolicy1.setHeightForWidth(self.x6.sizePolicy().hasHeightForWidth())
        self.x6.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x6, 1, 0, 1, 1)

        self.x4 = QPushButton(self.widget_9)
        self.x4.setObjectName(u"x4")
        sizePolicy1.setHeightForWidth(self.x4.sizePolicy().hasHeightForWidth())
        self.x4.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x4, 0, 1, 1, 1)

        self.x7 = QPushButton(self.widget_9)
        self.x7.setObjectName(u"x7")
        sizePolicy1.setHeightForWidth(self.x7.sizePolicy().hasHeightForWidth())
        self.x7.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x7, 1, 2, 1, 1)

        self.x3 = QPushButton(self.widget_9)
        self.x3.setObjectName(u"x3")
        sizePolicy1.setHeightForWidth(self.x3.sizePolicy().hasHeightForWidth())
        self.x3.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x3, 0, 0, 1, 1)

        self.x0 = QPushButton(self.widget_9)
        self.x0.setObjectName(u"x0")
        sizePolicy1.setHeightForWidth(self.x0.sizePolicy().hasHeightForWidth())
        self.x0.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x0, 2, 2, 1, 1)

        self.x9 = QPushButton(self.widget_9)
        self.x9.setObjectName(u"x9")
        sizePolicy1.setHeightForWidth(self.x9.sizePolicy().hasHeightForWidth())
        self.x9.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.x9, 2, 1, 1, 1)

        self.label_16 = QLabel(self.widget_9)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setStyleSheet(u"image: url(:/bg/res/beijing-subway.gif);")

        self.gridLayout_2.addWidget(self.label_16, 1, 1, 1, 1)


        self.horizontalLayout_8.addWidget(self.widget_9)


        self.verticalLayout_7.addWidget(self.widget_15)

        self.places = QWidget(MainWidget)
        self.places.setObjectName(u"places")
        self.horizontalLayout = QHBoxLayout(self.places)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.p_bank = QPushButton(self.places)
        self.p_bank.setObjectName(u"p_bank")
        sizePolicy1.setHeightForWidth(self.p_bank.sizePolicy().hasHeightForWidth())
        self.p_bank.setSizePolicy(sizePolicy1)
        self.p_bank.setStyleSheet(u"QPushButton{\n"
"icon: url(:/bg/res/bank.ico);\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"icon: url(:/bg/res/bank_hover.ico);\n"
"}")

        self.horizontalLayout.addWidget(self.p_bank)

        self.p_hospital = QPushButton(self.places)
        self.p_hospital.setObjectName(u"p_hospital")
        sizePolicy1.setHeightForWidth(self.p_hospital.sizePolicy().hasHeightForWidth())
        self.p_hospital.setSizePolicy(sizePolicy1)
        self.p_hospital.setStyleSheet(u"QPushButton{\n"
"icon: url(:/bg/res/hospital.ico);\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"icon: url(:/bg/res/hospital_hover.ico);\n"
"}")
        self.p_hospital.setFlat(False)

        self.horizontalLayout.addWidget(self.p_hospital)

        self.p_postoffice = QPushButton(self.places)
        self.p_postoffice.setObjectName(u"p_postoffice")
        sizePolicy1.setHeightForWidth(self.p_postoffice.sizePolicy().hasHeightForWidth())
        self.p_postoffice.setSizePolicy(sizePolicy1)
        self.p_postoffice.setStyleSheet(u"QPushButton{\n"
"icon: url(:/bg/res/postoffice.ico);\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"icon: url(:/bg/res/postoffice_hover.ico);\n"
"}")

        self.horizontalLayout.addWidget(self.p_postoffice)

        self.p_rent = QPushButton(self.places)
        self.p_rent.setObjectName(u"p_rent")
        sizePolicy1.setHeightForWidth(self.p_rent.sizePolicy().hasHeightForWidth())
        self.p_rent.setSizePolicy(sizePolicy1)
        self.p_rent.setStyleSheet(u"QPushButton{\n"
"icon: url(:/bg/res/rent.ico);\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"icon: url(:/bg/res/rent_hover.ico);\n"
"}")

        self.horizontalLayout.addWidget(self.p_rent)

        self.p_netcafe = QPushButton(self.places)
        self.p_netcafe.setObjectName(u"p_netcafe")
        sizePolicy1.setHeightForWidth(self.p_netcafe.sizePolicy().hasHeightForWidth())
        self.p_netcafe.setSizePolicy(sizePolicy1)
        self.p_netcafe.setStyleSheet(u"QPushButton{\n"
"icon: url(:/bg/res/netcafe.ico);\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"icon: url(:/bg/res/netcafe_hover.ico);\n"
"}")

        self.horizontalLayout.addWidget(self.p_netcafe)


        self.verticalLayout_7.addWidget(self.places)

        self.ticker = QTextBrowser(MainWidget)
        self.ticker.setObjectName(u"ticker")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ticker.sizePolicy().hasHeightForWidth())
        self.ticker.setSizePolicy(sizePolicy5)
        self.ticker.setMaximumSize(QSize(16777215, 40))
        self.ticker.setStyleSheet(u"background: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(50, 180, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"color: white;")
        self.ticker.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ticker.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ticker.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.verticalLayout_7.addWidget(self.ticker)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainWidget", u"Black Market", None))
        self.label_8.setText(QCoreApplication.translate("MainWidget", u"Buy", None))
        self.buy.setText(QCoreApplication.translate("MainWidget", u"==>", None))
        self.label_9.setText(QCoreApplication.translate("MainWidget", u"Sell", None))
        self.sell.setText(QCoreApplication.translate("MainWidget", u"<==", None))
        self.label_7.setText(QCoreApplication.translate("MainWidget", u"Your rented house", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWidget", u"Your Status", None))
        self.label_2.setText(QCoreApplication.translate("MainWidget", u"Cash", None))
        self.label_3.setText(QCoreApplication.translate("MainWidget", u"Savings", None))
        self.label_4.setText(QCoreApplication.translate("MainWidget", u"Debt", None))
        self.label_5.setText(QCoreApplication.translate("MainWidget", u"Health", None))
        self.label_6.setText(QCoreApplication.translate("MainWidget", u"Fame", None))
        self.switch_place.setText(QCoreApplication.translate("MainWidget", u"I want to visit \n"
"the capital", None))
        self.x1.setText(QCoreApplication.translate("MainWidget", u"Pingguoyuan", None))
        self.x2.setText(QCoreApplication.translate("MainWidget", u"Gongzhufen", None))
        self.switch_mode.setText(QCoreApplication.translate("MainWidget", u"Switch mode", None))
        self.x8.setText(QCoreApplication.translate("MainWidget", u"Changchun Street", None))
        self.x5.setText(QCoreApplication.translate("MainWidget", u"Dongzhimen", None))
        self.x6.setText(QCoreApplication.translate("MainWidget", u"Fuxingmen", None))
        self.x4.setText(QCoreApplication.translate("MainWidget", u"Jishuitan", None))
        self.x7.setText(QCoreApplication.translate("MainWidget", u"Jianguomen", None))
        self.x3.setText(QCoreApplication.translate("MainWidget", u"Xizhimen", None))
        self.x0.setText(QCoreApplication.translate("MainWidget", u"Beijing Railway \n"
"Station", None))
        self.x9.setText(QCoreApplication.translate("MainWidget", u"Chongwenmen", None))
        self.label_16.setText("")
        self.p_bank.setText(QCoreApplication.translate("MainWidget", u"Bank", None))
        self.p_hospital.setText(QCoreApplication.translate("MainWidget", u"Hospital", None))
        self.p_postoffice.setText(QCoreApplication.translate("MainWidget", u"Post Office", None))
        self.p_rent.setText(QCoreApplication.translate("MainWidget", u"Rental agency", None))
        self.p_netcafe.setText(QCoreApplication.translate("MainWidget", u"Cyber Cafe", None))
        self.ticker.setHtml(QCoreApplication.translate("MainWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Beijing News: Citizens reported that someone was selling counterfeit wine at the subway entrance | 12:09 | Guoly Computing company was established | 12:20 | Beijing issued management regulations for the online antiques market | 21:8.10 | Guoly Computing company launched &quot;Beijing Fushengji&quot; survival strategy Games | 13:10 | Guoly Computing "
                        "seeks venture capital (guoxh@hotmail.com) | 2:25.00 | Chengdu smuggled plane successfully bids for Beijingers | 2:45.50 | Capital agency: big predictions for Beijing property market next year | 3:55.00 | The auto industry is once again aggressively recruiting Beijing Automobile to pay a thousand-yuan adjustment | 13:6.25 | North Korea supports Beijing's bid to host the Olympics | 2:35 | Famous painter An Qianlei: A promise between Beijing and me | 8:28.30 | Discounted air tickets for 50 yuan You can fly from Beijing East to Changping | 16:2.30 | Beijing combines the ban on setting off fireworks and firecrackers with the love for animals | 13:35.00 | Beijing Computer Sports Lottery announced that the 1.2 billion grand prize was claimed by a man | 7:06.00 | Xicheng's &quot;anti-pornography&quot; The regular army takes action &quot;quickly, accurately and ruthlessly&quot; | 4:62.00 | Beijing police crack down on those who buy and sell fake cosmetics | 10:60.00 | Witnesses in Beijing: Vendors are rampant at subway"
                        " entrances, and people say the relevant departments should take control | 2:19.50 | Imported toys and electronics Business website (ePlayMe.com) launched in Beijing | 20:1.80 | 200,000 teachers and students in the capital signed in support of the Olympic bid | 23:1.00 | &quot;Beijing Pravda&quot; recruitment reporters will undergo re-examination on Saturday | 5:04.15 | Thousand-year-old wine appears in Beijing The fragrance of counterfeit wine is the best | 9:16.00 | High-tech development in rural areas: VCD sellers gather in the capital | 4:00.00 | Seven major trends in parallel-imported mobile phones in Beijing attract scientists' attention | 7:12:5 | Beijing's environmentally friendly toilets enter the United States | 23 :50 (US Western Time) | Three ears were cut off after a fellow villager turned against him | 5:40 | Police raided in the early morning and seized 5,000 copies of &quot;It Looks Really Fake&quot; | 4:08 | Beijing's new fashion: Give away lottery tickets during the holidays | 19: 45 | College"
                        " students working in Beijing proudly say: Our housing will be available for purchase in 100 years | 10:46 | Beijing has made great achievements in environmental protection, Shougang is more than 10 times more beautiful than the park | 7:13.00 | Citizen Uncle Zhang reflects that some people Selling &quot;Shanghai Baby&quot; at the subway entrance | 6:00 | The CEO of a company in Zhongguancun accidentally drank Shanxi fake liquor and passed out, and the date of entering NSDQ was postponed | 20:0.50 | &quot;Universal Qigong Daily&quot;: Registration for the crash course on sinking qi in Dantian has begun | 15 :50 | Public security in Beijing has reached a new level and it has been rated as the safest city in the world | 19:00.00 | Officials joked about why the phenomenon of arbitrary fees in Beijing disappeared | 20:00 | The Industry and Commerce Bureau investigated a pirated VCD den | 4:0:00 | American experts: Beijing\u2019s air contains a variety of minerals and is rich in nutrients | 8:15:00 (US Eastern Time)"
                        " | An expensive car turned out to be a smuggled car in Xiamen | 8:59:00 | College graduate job fair information: University of Posts and Telecommunications The supply of students exceeds the demand, and many IT companies are snatching people | 4:16:00 | Primary school students from all over the world gather in Beijing to see white pollution and sandstorms | 6:20:00 (Paris time) | Letter of thanks from Swan Lake: Beijingers saved wild swans | 6:18:00 | At the Hong Kong conference, Beijing was rated as the cleanest city | 6:48:00 | A good district chief who insists on &quot;putting relatives second and talents first&quot; | 2:32:85 | Experts say: FoxLoveChicken.com website will not go bankrupt and will be profitable in 2 years | 3:30 | Leaders say: Beijing\u2019s roads are in good condition | 4:07 | Citizens complain about too many fake medical advertisements in Beijing newspapers | 5:53 | Chen Gou Miss Cat's &quot;I Love Beijing's Hutongs&quot; won the first place in the essay competition | 4:40 | Community res"
                        "idents warned thieves: Stop stealing bicycles | 10:85 | A police station in Beijing was accused of moving someone else's household registration without permission | 4:00 | Beijing A university adheres to the lifelong system of &quot;doctoral supervisors&quot; and is praised by American professors | 19:09 | The 150th issue of the Beijing Sports Lottery draws a special prize of 20,000 first prize | 5:63 | Archaeological excavation of &quot;Yak Hutong&quot; in Beijing , the live TV broadcast turned into a farce | 10:09 | Restaurants and other service industries will extend their business hours during Teachers\u2019 Day in Beijing | 23:00 | Three hundred buildings in Beijing have achieved broadband access | 3:40 | Beijing public security improves the order of passenger transportation during the festival | 8:23 | There are millions of college students &quot;working&quot; in Zhongguancun | 2:00 | Our city's polluting enterprises have decreased by 12% compared with the previous year | 11:34 | The securities market ha"
                        "s achieved a new breakthrough and annual financing has exceeded the trillion mark for the first time | 20:40 | Today End of news, replay in one minute | 14:24</span></p></body></html>", None))
    # retranslateUi

