# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pay_debt.ui'
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

class Ui_PayDebt(object):
    def setupUi(self, PayDebt):
        if not PayDebt.objectName():
            PayDebt.setObjectName(u"PayDebt")
        PayDebt.resize(400, 300)
        self.verticalLayout = QVBoxLayout(PayDebt)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(PayDebt)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.widget_2 = QWidget(PayDebt)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.widget_2)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_2.addWidget(self.spinBox)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget = QWidget(PayDebt)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 38))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.horizontalSpacer_3 = QSpacerItem(54, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(PayDebt)
        self.pushButton_2.clicked.connect(PayDebt.close)

        self.pushButton_2.setDefault(True)


        QMetaObject.connectSlotsByName(PayDebt)
    # setupUi

    def retranslateUi(self, PayDebt):
        PayDebt.setWindowTitle(QCoreApplication.translate("PayDebt", u"Pay back the village chief", None))
        self.label.setText(QCoreApplication.translate("PayDebt", u"The village chief said on the phone: \"Tie Niu, you owe me %d yuan, pay me back!\"", None))
        self.label_2.setText(QCoreApplication.translate("PayDebt", u"How much do you owe?", None))
        self.pushButton.setText(QCoreApplication.translate("PayDebt", u"Conform", None))
        self.pushButton_2.setText(QCoreApplication.translate("PayDebt", u"Wait a few days.", None))
    # retranslateUi

