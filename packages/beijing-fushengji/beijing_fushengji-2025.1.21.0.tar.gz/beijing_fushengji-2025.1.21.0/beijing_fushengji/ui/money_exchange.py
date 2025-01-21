# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'money_exchange.ui'
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
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_MoneyExchange(object):
    def setupUi(self, MoneyExchange):
        if not MoneyExchange.objectName():
            MoneyExchange.setObjectName(u"MoneyExchange")
        MoneyExchange.resize(373, 197)
        self.verticalLayout = QVBoxLayout(MoneyExchange)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(MoneyExchange)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(self.widget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.spinBox)


        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(MoneyExchange)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 38))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(28, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 38))

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(MoneyExchange)
        self.pushButton_2.clicked.connect(MoneyExchange.close)

        QMetaObject.connectSlotsByName(MoneyExchange)
    # setupUi

    def retranslateUi(self, MoneyExchange):
        MoneyExchange.setWindowTitle(QCoreApplication.translate("MoneyExchange", u"Cash Transactions", None))
        self.label.setText(QCoreApplication.translate("MoneyExchange", u"<placeholder>", None))
        self.pushButton.setText(QCoreApplication.translate("MoneyExchange", u"Conform Transaction", None))
        self.pushButton_2.setText(QCoreApplication.translate("MoneyExchange", u"Cancel Transaction", None))
    # retranslateUi

