# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'airport.ui'
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

class Ui_Airport(object):
    def setupUi(self, Airport):
        if not Airport.objectName():
            Airport.setObjectName(u"Airport")
        Airport.resize(427, 352)
        self.verticalLayout = QVBoxLayout(Airport)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Airport)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Airport)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.widget = QWidget(Airport)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(133, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(133, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Airport)
        self.pushButton.clicked.connect(Airport.close)

        QMetaObject.connectSlotsByName(Airport)
    # setupUi

    def retranslateUi(self, Airport):
        Airport.setWindowTitle(QCoreApplication.translate("Airport", u"Capital Airport", None))
        self.label.setText(QCoreApplication.translate("Airport", u"Do you want to fly to the United States and build a global trade network?", None))
        self.label_2.setText(QCoreApplication.translate("Airport", u"In the upcoming version 2.0, you can engage in international trade between major cities in the world (New York, Tokyo, London, Paris, Shanghai, Mumbai, Singapore, and Pyongyang in North Korea).\n"
" Selling food to North Korea? Sell \u200b\u200bcosmetics from Paris? Selling Indian specialties in New York? Or import Southeast Asian fruits to Singapore?\n"
" The most exciting thing is probably in Tokyo! Reselling Japanese specialties - \"Despicable Medicine\" and \"Despicable Meatballs\"!", None))
        self.pushButton.setText(QCoreApplication.translate("Airport", u"OK", None))
    # retranslateUi

