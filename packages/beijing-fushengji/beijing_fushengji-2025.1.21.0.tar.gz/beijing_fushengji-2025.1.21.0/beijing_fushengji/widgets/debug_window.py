from PySide6 import QtWidgets, QtGui, QtCore
import os
import importlib
from beijing_fushengji.widgets.styled_widget import StyledWidget


class CompleterWidget(StyledWidget):
    def __init__(self):
        super().__init__()

        self.widgets = []
        self.selected_index = 0
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.words = []

        self.ref = None

    def slot_complete(self, obj, attr):
        self.prefix = obj
        try:
            obj = eval(obj, globals(), {"self": self.ref})
        except Exception as _e:
            self.show_selection([])
        else:
            attrs = dir(obj)
            result = []
            for i in attrs:
                if i.startswith(attr):
                    result.append(i)
            if len(result) == 1 and attr == result[0]:  # TODO: fix double return
                self.show_selection([])
            self.show_selection(result[:5])

    def show_selection(self, words):
        for w in self.widgets:
            w.setParent(None)
            self.layout().removeWidget(w)
        self.words = words
        if len(words) == 0:
            return
        self.selected_index = 0
        self.widgets = [QtWidgets.QLabel(x) for x in words]
        self.widgets[self.selected_index].setStyleSheet("color: green;")

        for w in self.widgets:
            self.layout().addWidget(w)

    def complete(self):
        if len(self.words) == 0:
            return ""
        word = self.prefix + "." + self.words[self.selected_index]
        self.show_selection([])
        return word

    def has_completion(self):
        return len(self.words) != 0

    def slot_up(self):
        if len(self.widgets) == 0:
            return
        self.widgets[self.selected_index].setStyleSheet("")
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = 0
        self.widgets[self.selected_index].setStyleSheet("color: green;")

    def slot_down(self):
        if len(self.widgets) == 0:
            return
        self.widgets[self.selected_index].setStyleSheet("")
        self.selected_index += 1
        if self.selected_index >= len(self.widgets):
            self.selected_index = len(self.widgets) - 1
        self.widgets[self.selected_index].setStyleSheet("color: green;")


class MyInput(QtWidgets.QLineEdit):
    """
    Custom input class for handling input history.
    """

    sig_up = QtCore.Signal()
    sig_down = QtCore.Signal()
    sig_return = QtCore.Signal()

    def __init__(self, completer):
        super().__init__()

        self.completer = completer

        self.textChanged.connect(self.text_changed)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Up:
            if self.completer.has_completion():
                self.completer.slot_up()
            else:
                self.sig_up.emit()
        elif event.key() == QtCore.Qt.Key.Key_Down:
            if self.completer.has_completion():
                self.completer.slot_down()
            else:
                self.sig_down.emit()
        elif event.key() == QtCore.Qt.Key.Key_Return:
            w = self.completer.complete()
            if w != "":
                self.setText(w)
            else:
                self.sig_return.emit()
        elif event.key() == QtCore.Qt.Key.Key_Escape:
            self.completer.complete()
        super().keyPressEvent(event)

    def text_changed(self):
        "some help"
        if len(self.text()) == 0:
            return
        text = self.text()
        if "." not in text:
            return
        pointer_pos = text.rfind(".")
        obj = text[:pointer_pos]
        attr = text[pointer_pos + 1 :]
        self.completer.slot_complete(obj, attr)


class DebugWidget(StyledWidget):
    "The main debug widget layout."

    sig_data = QtCore.Signal(list, list)

    def __init__(self, main_widget=None, commands=(), results=()):
        super().__init__()
        self.main = main_widget

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.commands_area = QtWidgets.QScrollArea()
        self.commands_area.setWidgetResizable(True)
        self.commands_area_contents = StyledWidget()
        self.commands_area.setWidget(self.commands_area_contents)
        self.commands_area_layout = QtWidgets.QVBoxLayout()
        self.commands_area_contents.setLayout(self.commands_area_layout)

        self.commands = list(commands)
        self.results = list(results)

        self.completer = CompleterWidget()
        self.completer.ref = self.main
        self.input = MyInput(self.completer)
        self.input.setFont(QtGui.QFont("Consolas", 12))
        self.input.sig_return.connect(self.r_eval)

        self.input.sig_up.connect(self.enumerate_previous_command)
        self.input.sig_down.connect(self.enumerate_next_command)

        self._layout.addWidget(self.commands_area)
        self._layout.addWidget(self.completer)
        self._layout.addWidget(self.input)
        self.input.setFocus()

        self.input_index = 0
        for i in range(len(self.commands)):
            command = QtWidgets.QLabel(self.commands[i])
            command.setWordWrap(True)
            command.setFont(QtGui.QFont("Consolas", 12))

            result = QtWidgets.QLabel(self.results[i])
            result.setFont(QtGui.QFont("Consolas", 12))
            result.setWordWrap(True)
            self.commands_area_contents.layout().addWidget(command)
            self.commands_area_contents.layout().addWidget(result)

    def enumerate_previous_command(self):
        if len(self.commands) == 0:
            return
        self.input_index -= 1
        if self.input_index < 0:
            self.input_index = 0
        command = self.commands[self.input_index]
        self.input.setText(command)

    def enumerate_next_command(self):
        if len(self.commands) == 0:
            return
        self.input_index += 1
        if self.input_index >= len(self.commands):
            self.input_index = len(self.commands) - 1

        command = self.commands[self.input_index]
        self.input.setText(command)

    def r_eval(self):
        data = self.input.text()
        self.input.setText("self")
        try:
            r = eval(data, globals(), {"self": self.completer.ref})
        except Exception as e:
            r = str(e)
            try:
                exec(data, globals(), {"self": self.completer.ref})
            except Exception as e2:
                print(e, e2)
            else:
                self.add_data(data, "eval")
        else:
            self.add_data(data, r)

    def add_data(self, command, result):
        self.commands.append(str(command))
        self.results.append(str(result))
        self.sig_data.emit(self.commands, self.results)
        self.refresh_display()
        self.input_index = len(self.commands)

    def refresh_display(self):
        command = QtWidgets.QLabel(self.commands[-1])
        command.setWordWrap(True)
        command.setFont(QtGui.QFont("Consolas", 12))

        result = QtWidgets.QLabel(self.results[-1])
        result.setFont(QtGui.QFont("Consolas", 12))
        result.setWordWrap(True)
        self.commands_area_contents.layout().addWidget(command)
        self.commands_area_contents.layout().addWidget(result)

        QtCore.QTimer.singleShot(200, self.scroll)

    def scroll(self):
        scroll_bar = self.commands_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


class DebugWindowReloader(StyledWidget):
    "check modified file, reload debug widget."

    def __init__(self, main=None):
        super().__init__()
        self.main = main

        self.setWindowTitle("Live Debugger")

        self.commands = []  # for persisting input history during reload
        self.results = []

        self.mtime = os.path.getmtime(__file__)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check)
        self.timer.start(1000)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.widget = DebugWidget(self.main, self.commands, self.results)
        self.widget.sig_data.connect(self.slot_data)
        self._layout.addWidget(self.widget)

        self.resize(600, 400)

    def check(self):
        mtime = os.path.getmtime(__file__)
        if mtime != self.mtime:
            self.mtime = mtime

            try:
                s = importlib.import_module("widgets.debug_window")
                s = importlib.reload(s)
            except Exception as _:
                pass
            else:
                try:
                    self.widget_2 = s.DebugWidget(
                        self.main, self.commands, self.results
                    )
                except Exception as _v:
                    pass
                else:
                    self._layout.removeWidget(self.widget)
                    self.widget.setParent(None)
                    self.widget = self.widget_2
                    self.widget.sig_data.connect(self.slot_data)
                    self._layout.addWidget(self.widget)

    def slot_data(self, commands, results):
        self.commands = commands
        self.results = results


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    widget = DebugWindowReloader()
    widget.show()
    app.exec()
