# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)
import beijing_fushengji.main_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1091, 678)
        self.new_game = QAction(MainWindow)
        self.new_game.setObjectName(u"new_game")
        self.top_players = QAction(MainWindow)
        self.top_players.setObjectName(u"top_players")
        self.settings = QAction(MainWindow)
        self.settings.setObjectName(u"settings")
        self.exit_game = QAction(MainWindow)
        self.exit_game.setObjectName(u"exit_game")
        self.bank = QAction(MainWindow)
        self.bank.setObjectName(u"bank")
        self.post_office = QAction(MainWindow)
        self.post_office.setObjectName(u"post_office")
        self.hospital = QAction(MainWindow)
        self.hospital.setObjectName(u"hospital")
        self.airport = QAction(MainWindow)
        self.airport.setObjectName(u"airport")
        self.rental_agency = QAction(MainWindow)
        self.rental_agency.setObjectName(u"rental_agency")
        self.cybercafe = QAction(MainWindow)
        self.cybercafe.setObjectName(u"cybercafe")
        self.beijing_intro = QAction(MainWindow)
        self.beijing_intro.setObjectName(u"beijing_intro")
        self.story = QAction(MainWindow)
        self.story.setObjectName(u"story")
        self.game_help = QAction(MainWindow)
        self.game_help.setObjectName(u"game_help")
        self.about = QAction(MainWindow)
        self.about.setObjectName(u"about")
        self.langChs = QAction(MainWindow)
        self.langChs.setObjectName(u"langChs")
        self.langEn = QAction(MainWindow)
        self.langEn.setObjectName(u"langEn")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1091, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(u"menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menu.addAction(self.new_game)
        self.menu.addAction(self.top_players)
        self.menu.addAction(self.settings)
        self.menu.addAction(self.exit_game)
        self.menu_2.addAction(self.bank)
        self.menu_2.addAction(self.post_office)
        self.menu_2.addAction(self.hospital)
        self.menu_2.addAction(self.airport)
        self.menu_2.addAction(self.rental_agency)
        self.menu_2.addAction(self.cybercafe)
        self.menu_3.addAction(self.beijing_intro)
        self.menu_3.addAction(self.story)
        self.menu_3.addAction(self.game_help)
        self.menu_3.addAction(self.about)
        self.menuLanguage.addAction(self.langChs)
        self.menuLanguage.addAction(self.langEn)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Beijing Life", None))
        self.new_game.setText(QCoreApplication.translate("MainWindow", u"new game", None))
        self.top_players.setText(QCoreApplication.translate("MainWindow", u"Ranking", None))
        self.settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.exit_game.setText(QCoreApplication.translate("MainWindow", u"exit", None))
        self.bank.setText(QCoreApplication.translate("MainWindow", u"Bank", None))
        self.post_office.setText(QCoreApplication.translate("MainWindow", u"Post Office", None))
        self.hospital.setText(QCoreApplication.translate("MainWindow", u"Hospital", None))
        self.airport.setText(QCoreApplication.translate("MainWindow", u"Airport", None))
        self.rental_agency.setText(QCoreApplication.translate("MainWindow", u"Rental Agency", None))
        self.cybercafe.setText(QCoreApplication.translate("MainWindow", u"Cyber Cafe", None))
        self.beijing_intro.setText(QCoreApplication.translate("MainWindow", u"Beijing Intro", None))
        self.story.setText(QCoreApplication.translate("MainWindow", u"Game Story", None))
        self.game_help.setText(QCoreApplication.translate("MainWindow", u"Game Guide", None))
        self.about.setText(QCoreApplication.translate("MainWindow", u"About this game", None))
        self.langChs.setText(QCoreApplication.translate("MainWindow", u"Chinese Simplified", None))
        self.langEn.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"System", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"Places", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
    # retranslateUi

