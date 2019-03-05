# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
class Instruction(QMainWindow):
    def __init__(self):
        super(Instruction,self).__init__()
        self.resize(475, 295)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("软件使用说明")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 80, 436, 100))
        self.label.wordWrap()
        self.label.setText("1.软件运行时会自动使用左边文件列的每一类的第一个文件作为素材使用。\n\n2.可右键文件，使用置顶功能将文件置顶。\n\n3.双击文件可以自动加载到右边列表中，修改后点击工具栏或菜单栏保存。\n\n4.程序运行前需选择要进行编码的列，否则默认编码第一列。")
    def Show(self):
        self.show()
if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainmenu = Instruction()
    mainmenu.Show()
    sys.exit(app.exec_())