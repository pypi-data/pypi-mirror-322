# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rent.ui'
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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Rent(object):
    def setupUi(self, Rent):
        if not Rent.objectName():
            Rent.setObjectName(u"Rent")
        Rent.resize(489, 261)
        Rent.setStyleSheet(u"QLabel, QPushButton{\n"
"                font: 12pt MiSans;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(Rent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Rent)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Rent)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.widget = QWidget(Rent)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(19, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ok = QPushButton(self.widget)
        self.ok.setObjectName(u"ok")
        self.ok.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.ok)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.cancel = QPushButton(self.widget)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.cancel)

        self.horizontalSpacer_3 = QSpacerItem(19, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Rent)

        QMetaObject.connectSlotsByName(Rent)
    # setupUi

    def retranslateUi(self, Rent):
        Rent.setWindowTitle(QCoreApplication.translate("Rent", u"Rental Agency", None))
        self.label.setText(QCoreApplication.translate("Rent", u"Welcome to Beijing \"Bianziju\" rental agency!\n"
"Our philosophy: free house viewing, additional payment after transaction, no one is cheated, shameless and fearless!", None))
        self.label_2.setText(QCoreApplication.translate("Rent", u"Want to expand your business? Your current house can only hold {} items, it's too small!\n"
"You can spend {} yuan to rent a house that can hold {} items.", None))
        self.ok.setText(QCoreApplication.translate("Rent", u"Transaction", None))
        self.cancel.setText(QCoreApplication.translate("Rent", u"Afraid of being cheated, try next time", None))
    # retranslateUi

