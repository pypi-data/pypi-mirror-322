# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hospital.ui'
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
import beijing_fushengji.main_rc

class Ui_Hospital(object):
    def setupUi(self, Hospital):
        if not Hospital.objectName():
            Hospital.setObjectName(u"Hospital")
        Hospital.resize(440, 259)
        self.verticalLayout = QVBoxLayout(Hospital)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Hospital)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(50, 16777215))
        self.widget.setStyleSheet(u"image: url(:/bg/res/icon1.ico);")

        self.verticalLayout.addWidget(self.widget)

        self.label_2 = QLabel(Hospital)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(Hospital)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.widget_2 = QWidget(Hospital)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(self.widget_2)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(Hospital)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(74, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(self.widget_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 38))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(73, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(self.widget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 38))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer_3 = QSpacerItem(74, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.widget_3)


        self.retranslateUi(Hospital)
        self.pushButton_2.clicked.connect(Hospital.close)

        QMetaObject.connectSlotsByName(Hospital)
    # setupUi

    def retranslateUi(self, Hospital):
        Hospital.setWindowTitle(QCoreApplication.translate("Hospital", u"In Hospital", None))
        self.label_2.setText(QCoreApplication.translate("Hospital", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("Hospital", u"Resolutely resist corruption! I will only charge you 3,500 yuan red envelope for each health point.\"", None))
        self.label.setText(QCoreApplication.translate("Hospital", u"Treatment Points", None))
        self.pushButton.setText(QCoreApplication.translate("Hospital", u"Confirm", None))
        self.pushButton_2.setText(QCoreApplication.translate("Hospital", u"You are too dark! I will sue you!", None))
    # retranslateUi

