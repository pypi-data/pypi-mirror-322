import os
import platform
import sys
import beijing_fushengji.widgets.mainwindow as mainwindow
from PySide6 import QtWidgets
import argparse
from beijing_fushengji.console.mainwindow import main as main_cli


def main_gui():
    if platform.system() == "Linux":
        # this will enable automaic load of fcitx plugin
        os.environ["QT_PLUGIN_PATH"] = (
            os.environ.get("QT_PLUGIN_PATH", "") + ";" + "/usr/lib/qt6/plugins/"
        )
    app = QtWidgets.QApplication(sys.argv)

    _window = mainwindow.MainWindow(app)
    _window.show()
    sys.exit(app.exec())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", action="store_true", default=False)
    args = parser.parse_args()
    if args.console:
        main_cli()
    else:
        main_gui()


if __name__ == "__main__":
    main()
