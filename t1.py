# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 15:42:21 2017

@author: 李莘
"""
import copy
import time
import sys
from threading import Thread
import pandas as pd
import numpy as np
import multiprocessing as mp
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtCore import QObject, QThread, Qt
from PyQt5 import QtCore, QtWidgets, QtGui


class A(QThread):  
    trigger = pyqtSignal(str)  
    def __int__(self):  
        super(A,self).__init__()  
  
    def run(self):
        x='1234'
        self.trigger.emit(x) 
        
class L(QtWidgets.QLabel):
    def __init__(self, txt, parent  = None):
        super(L, self).__init__(parent)
        self.setText(txt)

    def setTxt(self, s):
        self.setText(s)
        
class W(QtWidgets.QWidget):
    def __init__(self, thread, parent  = None):
        super(W, self).__init__(parent)
        self.t = thread
        
        self.lay = QtWidgets.QVBoxLayout(self)
        self.l = L('xxxx', self)
        self.button= QtWidgets.QPushButton('mmmp', self)
        self.lay.addWidget(self.l)
        self.lay.addWidget(self.button)
        
        self.t.trigger.connect(self.l.setTxt)
        self.button.clicked.connect(self.t.start)
        
    def f(self, txt):
        self.l.setText(txt)
        
def main():
    
    app = QtWidgets.QApplication([])
    a = A()
    w = W(a)
    
    w.show()
    app.exec_()

if __name__ == "__main__":
     
    main()

'''
from PyQt5.QtCore import *  
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *  
  
class WorkThread(QThread):  
    trigger = pyqtSignal(str)  
    def __int__(self):  
        super(WorkThread,self).__init__()  
  
    def run(self):  
        x='1234'
        self.trigger.emit(x) 
  
def work():  
    workThread.trigger.connect(label.setText)
    workThread.start()     
    
app=QApplication([])  
top=QWidget()  

layout=QVBoxLayout(top)   
label = QtWidgets.QLabel('xxxxx')
button=QPushButton("测试")  
layout.addWidget(label)  
layout.addWidget(button)  

workThread=WorkThread()  
button.clicked.connect(work)
  
top.show()  
app.exec()  
'''







