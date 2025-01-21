# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'statements.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Statements(object):
    def setupUi(self, Statements):
        if not Statements.objectName():
            Statements.setObjectName(u"Statements")
        Statements.resize(618, 581)
        self.gridLayout = QGridLayout(Statements)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(Statements)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(233, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget_3)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_3)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Statements)
        self.pushButton.clicked.connect(Statements.close)

        QMetaObject.connectSlotsByName(Statements)
    # setupUi

    def retranslateUi(self, Statements):
        Statements.setWindowTitle(QCoreApplication.translate("Statements", u"---", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Statements", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'MiSans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Special statement about this game</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">1. The plots, scenes and ways of doing things described in this game are purely fictitious and have no allusion to reality. Not a"
                        "ll rental agencies in Beijing are fraudulent, just as not all officials are corrupt.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">2. Some of the attributes of items in this game (smuggled goods, counterfeit goods, banned books) and certain player behaviors set by the game (reselling items prohibited by law) are illegal and unacceptable in real society and morality. Therefore, this game is prohibited from being played by people under the age of 20 who have not yet established a sense of right and wrong. People of other ages must understand the virtual nature of the game, the illegality of smuggling and counterfeiting, and abide by all national laws and regulations when playing this game.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt"
                        ";\">3. This game is free software, and individual players can freely copy, download and reproduce it, and can recommend it to adults over 20 years old.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">4. Welcome website to provide free download service of this game. However, before providing download services, the author's written consent must be obtained, unless the author actively contacts the website. Machine pre-installation, integration, CD sales, gifts, or any other commercial profit-making activities based on this game must obtain the author's written consent. The free download services or other commercial profit-making activities based on this game involved in this article must ensure the integrity and consistency of the game information. This game (including the game's name, version, author information, binary program code and other arbitrary files, etc.) is not a"
                        "llowed to be modified in any form.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">5. When released as free software, we are not responsible for providing any form of technical support for this game, and believe that this software has no warranty (no warranty)</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("Statements", u"OK", None))
    # retranslateUi

