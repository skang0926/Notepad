import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore

form_class = uic.loadUiType("notepad.ui")[0]


class findWindow(QDialog):
    def __init__(self, parent):
        super(findWindow, self).__init__(parent)
        uic.loadUi("find.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancle.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
            # print("up")
        elif self.radioButton_down.isChecked():
            self.up_down = "down"
            # print("down")

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSenesitive.isChecked():
            cs = QtCore.Qt.CaseSensitive
        else:
            cs = QtCore.Qt.CaseInsensitive

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos)
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1):
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        ret = msgBox.exec_()

class changeWindow(QDialog):
    def __init__(self, parent):
        super(changeWindow, self).__init__(parent)
        uic.loadUi("change.ui", self)

        self.pushButton_cancle.clicked.connect(self.close)
        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_change.clicked.connect(self.change)
        self.pushButton_allchange.clicked.connect(self.allChange)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        pos = self.cursor.position()
        index = reg.indexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1):
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def change(self):
        pattern = self.lineEdit.text()
        changeText = self.lineEdit_change.text()


        text = self.pe.toPlainText()

        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()
        pos = self.cursor.position()

        index = reg.indexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1):
            replaceText = text.replace(pattern, changeText, 1)
            self.pe.setPlainText(replaceText)
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def allChange(self):
        pattern = self.lineEdit.text()
        changeText = self.lineEdit_change.text()

        text = self.pe.toPlainText()

        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()
        pos = self.cursor.position()

        index = reg.indexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1):
            replaceText = text.replace(pattern, changeText)
            self.pe.setPlainText(replaceText)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        ret = msgBox.exec_()

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveas.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)

        self.action_find.triggered.connect(self.findFunction)
        self.action_change.triggered.connect(self.changeFunction)

        self.opened = False
        self.opened_file_path = '제목 없음'

    def ischanged(self):
        if not self.opened:
            print('a')
            if self.plainTextEdit.toPlainText().strip():
                return True
            return False

        # 현재 데이터
        current_data = self.plainTextEdit.toPlainText()

        # 파일에 저장된 데이터
        with open(self.opened_file_path, encoding='UTF8') as f:
            file_data = f.read()

        if current_data == file_data:
            return False
        else:
            return True

    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole)  # 0
        msgBox.addButton('저장 안 함', QMessageBox.NoRole)  # 1
        msgBox.addButton('취소', QMessageBox.RejectRole)  # 2
        ret = msgBox.exec_()

        if ret == 0:
            self.saveFunction()
        else:
            return ret

    def closeEvent(self, event):
        if self.ischanged():
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()

    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()

        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)

        self.opened = True
        self.opened_file_path = fname

        print("save {}!!".format(fname))

    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()

        self.plainTextEdit.setPlainText(data)

        self.opened = True
        self.opened_file_path = fname

        print("open {}!!".format(fname))

    def openFunction(self):
        if self.ischanged():
            ret = self.save_changed_data()

        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plainTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def findFunction(self):
        findWindow(self)

    def changeFunction(self):
        changeWindow(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()
