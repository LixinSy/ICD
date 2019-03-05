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

class Aboutus(QMainWindow):
    def __init__(self):
        super(Aboutus,self).__init__()
        self.resize(425, 209)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("医疗诊断数据清洗与自动编码")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 60, 336, 12))
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 78, 12))
        self.setWindowTitle("关于我们")
        self.label.setText("软件作者：成都信息工程大学-李莘，成都信息工程大学-谢雨杉")
        self.label_2.setText("时间：2017.10")
    def Show(self):
        self.show()
if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainmenu = Aboutus()
    mainmenu.Show()
    sys.exit(app.exec_())