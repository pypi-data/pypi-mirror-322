# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bank.ui'
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

class Ui_Bank(object):
    def setupUi(self, Bank):
        if not Bank.objectName():
            Bank.setObjectName(u"Bank")
        Bank.resize(407, 176)
        self.verticalLayout = QVBoxLayout(Bank)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Bank)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(Bank)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.deposit = QPushButton(self.widget)
        self.deposit.setObjectName(u"deposit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deposit.sizePolicy().hasHeightForWidth())
        self.deposit.setSizePolicy(sizePolicy)
        self.deposit.setMaximumSize(QSize(16777215, 38))

        self.horizontalLayout.addWidget(self.deposit)

        self.withdraw = QPushButton(self.widget)
        self.withdraw.setObjectName(u"withdraw")
        sizePolicy.setHeightForWidth(self.withdraw.sizePolicy().hasHeightForWidth())
        self.withdraw.setSizePolicy(sizePolicy)
        self.withdraw.setMaximumSize(QSize(16777215, 38))

        self.horizontalLayout.addWidget(self.withdraw)

        self.leave = QPushButton(self.widget)
        self.leave.setObjectName(u"leave")
        sizePolicy.setHeightForWidth(self.leave.sizePolicy().hasHeightForWidth())
        self.leave.setSizePolicy(sizePolicy)
        self.leave.setMaximumSize(QSize(16777215, 38))
        self.leave.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.leave)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Bank)
        self.leave.clicked.connect(Bank.close)

        self.leave.setDefault(True)


        QMetaObject.connectSlotsByName(Bank)
    # setupUi

    def retranslateUi(self, Bank):
        Bank.setWindowTitle(QCoreApplication.translate("Bank", u"Bank!", None))
        self.label.setText(QCoreApplication.translate("Bank", u"Hello customer! Your cash is 2000, your deposit is 0, what do you want to do...", None))
        self.deposit.setText(QCoreApplication.translate("Bank", u"Deposit", None))
        self.withdraw.setText(QCoreApplication.translate("Bank", u"Withdraw", None))
        self.leave.setText(QCoreApplication.translate("Bank", u"Leave", None))
    # retranslateUi

