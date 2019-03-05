# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:25:35 2017

@author: 李莘
"""
import time
import os
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
import file
'''
d = file.File(r'./data/dd.txt').Read()
print(type(d))
for w in d:
    if w == '\\':
        print(1111)

with open(r'./data/del.txt', 'w', encoding = 'utf-8') as f:
    f.write(' `~!@#$%^&*-_=+(){}[];:<>,.?·~（）【】；：《》，。？、‘’“”并及和与病症的性\'\"\\')

'''

def main():
    
    app = QtWidgets.QApplication([])
    #w = QtWidgets.QTableWidget()
    m = QtGui.QStandardItemModel()
    m.setRowCount(10)
    m.setColumnCount(5)
    #m.setHorizontalHeaderLabels(['11','22','33','44'])
    
    it = QtGui.QStandardItem('xxxxxxxxxxx')
    m.setHorizontalHeaderItem(0,it)
    m.setHorizontalHeaderItem(1,QtGui.QStandardItem('abcd'))
    m.setHorizontalHeaderItem(2,QtGui.QStandardItem('abcd'))
    m.setHorizontalHeaderItem(3,QtGui.QStandardItem('abcd'))
    m.setHorizontalHeaderItem(4,QtGui.QStandardItem('abcd'))
    I = m.horizontalHeaderItem(it.column())
    m.setItem(2,1,it)
    #print(it.column(), I.text())
    
    w = QtWidgets.QTableView()
    w.setModel(m)
    w.selectColumn(1)
    print(m.horizontalHeaderItem(w.columnAt(0)).text())
    print(w.columnViewportPosition(0))

    '''
    w.setColumnCount(5)
    w.setHorizontalHeaderItem(0,item)
    '''
    w.show()
    app.exec_()

if __name__ == "__main__":
     
    main()
    
    
    
    
    