from PySide6 import QtWidgets, QtGui, QtCore
import beijing_fushengji.ui.mainwindow as ui_mainwindow
import beijing_fushengji.widgets.main_widget as main_widget
from beijing_fushengji.app.tools import load


class MainWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        self.widget.save()
        super().closeEvent(event)

    def __init__(self, app):
        super().__init__()
        QtWidgets.QApplication.setOrganizationName("SodaCris")
        QtWidgets.QApplication.setOrganizationDomain("sodacris.com")
        QtWidgets.QApplication.setApplicationName("Beijing Fushengji")
        from beijing_fushengji.widgets.styled_widget import qss

        self.setStyleSheet(qss)

        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))

        self.app = app
        self.settings = QtCore.QSettings()
        lang = self.settings.value("lang", "cn")
        if lang == "cn":
            self.translator = QtCore.QTranslator()
            self.translator.load(":/translations/cn.qm")
            self.app.installTranslator(self.translator)
        self.init()

        from beijing_fushengji.app.tools import debugger_is_active

        if debugger_is_active():
            from beijing_fushengji.widgets.debug_window import DebugWindowReloader

            self.debug_window = DebugWindowReloader(self.widget)
            self.debug_window.show()

    def lang_chs(self):
        self.settings.setValue("lang", "cn")
        QtWidgets.QMessageBox.information(
            None, "Info", "重启游戏即可生效", QtWidgets.QMessageBox.Ok
        )

    def lang_en(self):
        self.settings.setValue("lang", "en")
        QtWidgets.QMessageBox.information(
            None, "Info", "restart game to take effect", QtWidgets.QMessageBox.Ok
        )

    def init(self):
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        from beijing_fushengji.widgets.styled_widget import qss

        self.setStyleSheet(qss)
        self.widget = main_widget.MainWidget()
        self.widget.hide()
        self.widget.sig_time_pass.connect(self.set_title)
        self.set_title(self.widget.time_left)
        self.widget.sig_close.connect(self.close)
        self.setCentralWidget(self.widget)
        self.widget.show()

        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.ui.menubar.setFont(QtGui.QFont(family, 14))
        self.ui.menu.setFont(QtGui.QFont(family, 14))
        self.ui.menu_2.setFont(QtGui.QFont(family, 14))
        self.ui.menu_3.setFont(QtGui.QFont(family, 14))

        self.ui.post_office.triggered.connect(self.widget.pay_debt)
        self.ui.hospital.triggered.connect(self.widget.enter_hospital)
        self.ui.bank.triggered.connect(self.widget.enter_bank)
        self.ui.about.triggered.connect(self.widget.show_about)
        self.ui.airport.triggered.connect(self.widget.go_airport)
        self.ui.settings.triggered.connect(self.widget.show_settings)
        self.ui.exit_game.triggered.connect(self.widget.close)
        self.ui.exit_game.triggered.connect(self.close)
        self.ui.cybercafe.triggered.connect(self.widget.enter_cafe)
        self.ui.top_players.triggered.connect(self.widget.show_top_players)
        self.ui.new_game.triggered.connect(self.widget.on_new_game)
        self.ui.rental_agency.triggered.connect(self.widget.rent_house)
        self.ui.beijing_intro.triggered.connect(self.beijing_intro)
        self.ui.game_help.triggered.connect(self.game_doc)
        self.ui.story.triggered.connect(self.show_story)
        self.ui.langChs.triggered.connect(self.lang_chs)
        self.ui.langEn.triggered.connect(self.lang_en)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check)
        # self.timer.start()

    def show_story(self):
        from beijing_fushengji.widgets.story import StoryDlg

        self.d_story = StoryDlg(c_continue=True)
        self.d_story.show()

    def game_doc(self):
        import webbrowser

        webbrowser.open(str(self.widget.d_story.help_file))

    def beijing_intro(self):
        self.intro = load("widgets.simple_dialogs").BeijingIntro()
        self.intro.show()

    def set_title(self, time_left: int):
        self.setWindowTitle(
            self.tr("Beijing Life ({}/{} day)").format(40 - time_left, 40)
        )

    def check(self):
        from pathlib import Path

        CURRENT = Path(__file__).resolve().parent
        reload_action = CURRENT.parent.joinpath("ui/_reload")

        self.app.removeTranslator(self.translator)
        self.translator.load("translation_zh_CN.qm")
        self.app.installTranslator(self.translator)

        if reload_action.exists():
            reload_action.unlink()
            import importlib

            importlib.reload(main_widget)
            self.widget.setParent(None)
            self.widget = main_widget.MainWidget()
            self.setCentralWidget(self.widget)
