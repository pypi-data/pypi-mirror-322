# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'net_cafe.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_CyberCafe(object):
    def setupUi(self, CyberCafe):
        if not CyberCafe.objectName():
            CyberCafe.setObjectName(u"CyberCafe")
        CyberCafe.resize(432, 444)
        CyberCafe.setAcceptDrops(False)
        self.verticalLayout = QVBoxLayout(CyberCafe)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(CyberCafe)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.groupBox = QGroupBox(CyberCafe)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(CyberCafe)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setOpenExternalLinks(True)

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget = QWidget(CyberCafe)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(135, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.leave_cybercafe = QPushButton(self.widget)
        self.leave_cybercafe.setObjectName(u"leave_cybercafe")
        self.leave_cybercafe.setMinimumSize(QSize(0, 38))

        self.horizontalLayout.addWidget(self.leave_cybercafe)

        self.horizontalSpacer_2 = QSpacerItem(135, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(CyberCafe)

        self.leave_cybercafe.setDefault(True)


        QMetaObject.connectSlotsByName(CyberCafe)
    # setupUi

    def retranslateUi(self, CyberCafe):
        CyberCafe.setWindowTitle(QCoreApplication.translate("CyberCafe", u"Cyber Cafe", None))
        self.label.setText(QCoreApplication.translate("CyberCafe", u"Please choose what to do in cybercafe:", None))
        self.groupBox.setTitle(QCoreApplication.translate("CyberCafe", u"About this game:", None))
        self.label_2.setText(QCoreApplication.translate("CyberCafe", u"<html><head/><body><p>Write email to author: <a href=\"mailto:guoxh@hotmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">mailto:guoxh@hotmail.com</span></a></p><p><a href=\"mailto:guoxh@hotmail.com\"></a><span>Join discuss group, get latest version and news:</span></p><p><a href=\"http://groups.yahoo.com/group/BeijingHell\"><span style=\" text-decoration: underline; color:#0000ff;\">http://groups.yahoo.com/group/BeijingHell</span></a></p><p>Access main page of this game:</p><p><a href=\"http://www.guoly.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.guoly.com</span></a></p><p><a href=\"http://guolycomtypeb.51.net\"><span style=\" text-decoration: underline; color:#0000ff;\">http://guolycomtypeb.51.net</span></a></p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("CyberCafe", u"About game:", None))
        self.label_3.setText(QCoreApplication.translate("CyberCafe", u"<html><head/><body><p>Free game: <a href=\"http://www.freegames.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.freegames.com</span></a></p><p>Game development: <a href=\"http://www.gamedev.net\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.gamedev.net</span></a></p></body></html>", None))
        self.leave_cybercafe.setText(QCoreApplication.translate("CyberCafe", u"Leave Cybercafe", None))
    # retranslateUi

