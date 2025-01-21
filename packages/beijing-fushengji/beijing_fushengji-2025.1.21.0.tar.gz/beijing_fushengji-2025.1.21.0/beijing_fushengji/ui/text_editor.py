# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_TextEditor(object):
    def setupUi(self, TextEditor):
        if not TextEditor.objectName():
            TextEditor.setObjectName(u"TextEditor")
        TextEditor.resize(1050, 721)
        self.verticalLayout = QVBoxLayout(TextEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(TextEditor)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.widget = QWidget(TextEditor)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(30, -1, 30, -1)
        self.save = QPushButton(self.widget)
        self.save.setObjectName(u"save")

        self.horizontalLayout.addWidget(self.save)

        self.check_grammar = QPushButton(self.widget)
        self.check_grammar.setObjectName(u"check_grammar")

        self.horizontalLayout.addWidget(self.check_grammar)

        self.ok = QPushButton(self.widget)
        self.ok.setObjectName(u"ok")

        self.horizontalLayout.addWidget(self.ok)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(TextEditor)
        self.ok.clicked.connect(TextEditor.close)

        QMetaObject.connectSlotsByName(TextEditor)
    # setupUi

    def retranslateUi(self, TextEditor):
        TextEditor.setWindowTitle(QCoreApplication.translate("TextEditor", u"Writing", None))
        self.textEdit.setHtml(QCoreApplication.translate("TextEditor", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'MiSans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Some specific ideas about doing a good job this month</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">1. Adhere to doing your job well and further grasp the coordination tasks in business and technology. Work sh"
                        "ould be focused.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">2. Listen to colleagues' opinions humbly. This is very important.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">3. My current work situation is very good, but I must strive for better and improve my ability endlessly.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">4. Be proactive, positive, make plans, complete plans on time, and ask yourself every day: How am I doing at work?</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" fon"
                        "t-family:'Sans'; font-size:10pt;\">5. The boss and manager are very capable, and they care about me very much. I must work hard.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">6. After get off work every day, clean up your desk, because cleanliness helps to create a high-efficiency working atmosphere and gives people a feeling of fresh air.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">7. At midnight every Saturday, you should think about what to do next week, and it is best to put the easier things on Thursday afternoon, so that you will be full of energy for half a week.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-fami"
                        "ly:'Sans'; font-size:10pt;\">8. Don't speak and do things on your own. The manager and boss should give instructions on important matters. They are absolutely right.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans'; font-size:10pt;\"><br /></p></body></html>", None))
        self.save.setText(QCoreApplication.translate("TextEditor", u"Save", None))
        self.check_grammar.setText(QCoreApplication.translate("TextEditor", u"Check Grammar", None))
        self.ok.setText(QCoreApplication.translate("TextEditor", u"OK", None))
    # retranslateUi

