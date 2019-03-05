# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 12:27:57 2017

@author: 李莘
"""

import os
import time
from file import File
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
import myWidgets

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, mainWorker):
        super().__init__()
        #添加数据成员
        self.root = os.getcwd()
        self.conf = {u'标准ICD-10':'stdICD-10.csv' \
                     , u'替换词表':'swap.xlsx'  \
                     , u'删除词表':'del.txt' \
                     , u'分词词典':'dd.txt' }
        self.dockLeft = QtWidgets.QDockWidget(self)
        self.dockMiddle = QtWidgets.QDockWidget(self)
        self.dockRight = QtWidgets.QDockWidget(self)
        self.dockBottom = QtWidgets.QDockWidget(self)
        self.tabWidget = myWidgets.TabWidget(self.dockMiddle)
        self.mainWorker = mainWorker
        self.colTable = None
        self.hasDockRight = False
        #初始化界面
        self.resize(840, 600)
        self.initMenuBar()
        self.initToolBar()
        self.initTree()
        self.initDockWidget()
        self.initStatusBar()
        self.setWindowTitle('ICD编码')
        
    def initMenuBar(self):
        #初始化菜单栏
        menubar = self.menuBar()
        
        #file菜单内容
        act1 = QtWidgets.QAction(u'打开文件', self)
        act1.setShortcut('CTRL+O')
        act1.triggered.connect(self.openFile)
        act2 = QtWidgets.QAction(u'保存', self)
        act2.setShortcut('CTRL+S')
        act5 = QtWidgets.QAction(u'保存全部', self)
        act5.setShortcut('CTRL+SHIFT+A')
        #stdICD菜单内容
        act3 = QtWidgets.QAction(u'清洗', self)
        act4 = QtWidgets.QAction(u'搜索', self)
        #添加file菜单
        fileMenu = menubar.addMenu(u'&文件') 
        fileMenu.addAction(act1)
        fileMenu.addAction(act2)
        fileMenu.addAction(act5)
        #添加stdICD菜单
        stdICD_menu = menubar.addMenu(u'&标准ICD-10')
        stdICD_menu.addAction(act3)
        stdICD_menu.addAction(act4)
        #添加设置菜单
        act6 = QtWidgets.QAction(u'字体', self) 
        setting_menu = menubar.addMenu(u'设置')
        setting_menu.addAction(act6)
        #关于菜单
        act7 = QtWidgets.QAction(u'软件使用说明', self)
        act8 = QtWidgets.QAction(u'关于我们...', self)
        setting_menu = menubar.addMenu(u'关于')
        setting_menu.addAction(act7)
        setting_menu.addAction(act8)
        
    def initToolBar(self):
        #初始化工具栏
        toolbar = QtWidgets.QToolBar(self)
        
        #打开文件工具
        actOfTool1 = QtWidgets.QAction(self)
        actOfTool1.setIcon(QtGui.QIcon('./source/7.png'))
        actOfTool1.setToolTip('Open file (CTRL+O)')
        actOfTool1.setShortcut('CTRL+O')
        actOfTool1.triggered.connect(self.openFile)
        #保存文件工具
        actOfTool2 = QtWidgets.QAction(self)
        actOfTool2.setIcon(QtGui.QIcon('./source/6.png'))
        actOfTool2.setToolTip('Save file (CTRL+S)')
        actOfTool2.setShortcut('CTRL+S')
        #开始匹配工具
        actWorkStart = QtWidgets.QAction(self)
        actWorkStart.setIcon(QtGui.QIcon('./source/9.png'))
        actWorkStart.setToolTip('start work (CTRL+ALT+S)')
        actWorkStart.setShortcut('CTRL+ALT+S')
        actWorkStart.triggered.connect(self.startWork)
        #添加工具
        toolbar.addAction(actOfTool1)
        toolbar.addAction(actOfTool2)
        toolbar.addAction(actWorkStart)
        self.addToolBar(toolbar)
    def initTree(self):
        #初始化树形列表
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.itemDoubleClicked.connect(self.openConfFile)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["文件列表"])
        self.tree.header().setStyleSheet("QHeaderView::section {background-color:skyblue;color: black;border: none;}")
        self.tree.setGeometry(QtCore.QRect(0, 56, 150, 500))
        
        #设置配置文件的树形列表
        rootOfconf = QtWidgets.QTreeWidgetItem(self.tree)
        rootOfconf.setText(0, u'配置文件')
        stdICD = myWidgets.ConfTreeItem(self.conf[u'标准ICD-10'], rootOfconf)
        stdICD.setText(0, u'标准ICD-10')
        stdICD.setToolTip(0, self.conf[u'标准ICD-10'])
        wordDict = myWidgets.ConfTreeItem(self.conf[u'分词词典'], rootOfconf)
        wordDict.setText(0, u'分词词典')
        wordDict.setToolTip(0, self.conf[u'分词词典'])
        replace = myWidgets.ConfTreeItem(self.conf[u'替换词表'], rootOfconf)
        replace.setText(0, u'替换词表')
        replace.setToolTip(0, self.conf[u'替换词表'])
        delWords = myWidgets.ConfTreeItem(self.conf[u'删除词表'], rootOfconf)
        delWords.setText(0, u'删除词表')
        delWords.setToolTip(0, self.conf[u'删除词表'])
        
        #设置用户文件的树形列表
        rootOfuser = myWidgets.UserTreeItem(self.tree)
        rootOfuser.setText(0, '用户文件')
        self.tabWidget.addTreeSignal.connect(rootOfuser.isAddChild)
        
    def initDockWidget(self):
        #初始化dockWidget
        ############设置dockLeft
        dockLeft = self.dockLeft#QtWidgets.QDockWidget(self)
        dockLeft.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        dockLeft.setWindowTitle('相关文件')
        dockLeft.setWidget(self.tree)
        dockLeft.setMaximumWidth(200)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockLeft)
        
        ############设置dockRight
        dockMiddle = self.dockMiddle#QtWidgets.QDockWidget(self)
        dockMiddle.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        dockMiddle.setWindowTitle(u'编辑')
        dockMiddle.setWidget(self.tabWidget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockMiddle)
        
        ############设置dockbottom
        dockBottom = self.dockBottom#QtWidgets.QDockWidget(self)
        dockBottom.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        dockBottom.setMaximumHeight(100)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dockBottom)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        dockBottom.setWidget(self.textBrowser)
        self.tabWidget.textSignal.connect(self.textBrowser.append)

    def initStatusBar(self):
        #添加状态栏
        statusBar = QtWidgets.QStatusBar(self)
        statusBar.setStyleSheet("QStatusBar{border: 1px; margin: 0px;width:100%;}")
        self.setStatusBar(statusBar)
    
    def openFile(self):
        #打开文件对话框，选取要读的文件（csv， Excel, txt）
        fpath = QtWidgets.QFileDialog.getOpenFileName(self, 'open file', \
                                            './data', \
                                            'All files(*);;Txt files(*.csv);;Excel files(*xlsx)')
        #判断是否有数据读入
        if not fpath[0]:
            return
        #不同文件有不同读取方式
        fname = fpath[0].split('/')[-1]
        self.textBrowser.append('打开' + fname)
        if fname.endswith('.csv'):
            #读取csv文件
            progressBar = QtWidgets.QProgressBar(self)
            progressBar.setStyleSheet("QProgressBar{border: 1px; margin: 0px;width:100%;}")
            self.statusBar().addWidget(progressBar)

            #定义表格呈现数据
            tableWidget = myWidgets.TableWidget(fpath[0], self)
            tableWidget.columnSignal.connect(self.showColumns)
            tableWidget.progressBarRangeSignal.connect(progressBar.setRange)
            tableWidget.progressBarValueSignal.connect(progressBar.setValue)
            tableWidget.progressBarDelSignal.connect(progressBar.deleteLater)
            tableWidget.mainWorkSetSignal.connect(self.tabWidget.setWorkWidget)
            tableWidget.textSignal.connect(self.textBrowser.append)
            self.tabWidget.addTab(tableWidget, fname)
            self.tabWidget.addedWidget(fname)
            self.tabWidget.setCurrentWidget(tableWidget)
            self.tabWidget.parentWidget().setWindowTitle(fpath[0])
            
        elif fname.endswith('.xlsx') or fname.endswith('.xls'):
            #读取excel文件
            progressBar = QtWidgets.QProgressBar(self)
            self.statusBar().addWidget(progressBar)
            #定义数据模型
            model = myWidgets.Model(fpath[0])
            model.progressBarRangeSignal.connect(progressBar.setRange)
            model.progressBarValueSignal.connect(progressBar.setValue)
            model.progressBarDelSignal.connect(progressBar.deleteLater)
            model.itemChanged.connect(self.tabWidget.changeTabTitle)
            model.savedSignal.connect(self.tabWidget.setPrimaryTabTitle)
            model.setData()
            #定义表格呈现数据
            table = myWidgets.TableView(model, self)
            self.tabWidget.addTab(table, fname)
            self.tabWidget.addedWidget(fname)
            self.tabWidget.setCurrentWidget(table)
            self.tabWidget.parentWidget().setWindowTitle(fpath[0])
            
        elif fname.endswith('.txt'):
            #读取文本文件
            progressBar = QtWidgets.QProgressBar(self)
            self.statusBar().addWidget(progressBar)
            #文本编辑器
            textEdit = myWidgets.TextEdit(fpath[0], self)
            textEdit.textChanged.connect(self.tabWidget.changeCurentTabTiltle)
            textEdit.textSignal.connect(self.textBrowser.append)
            textEdit.savedSignal.connect(self.tabWidget.setPrimaryTabTitle)
            textEdit.progressBarRangeSignal.connect(progressBar.setRange)
            textEdit.progressBarValueSignal.connect(progressBar.setValue)
            textEdit.progressBarDelSignal.connect(progressBar.deleteLater)
            textEdit.setData()
            self.tabWidget.addTab(textEdit, fname)
            self.tabWidget.addedWidget(fname)
            self.tabWidget.setCurrentWidget(textEdit)
            self.tabWidget.parentWidget().setWindowTitle(fpath[0])
        else:
            message = QtWidgets.QMessageBox(self)
            message.setWindowTitle(u'文件读取出错')
            message.setText(u'不支持打开该文件！')
            message.show()
    
    def openConfFile(self, treeItem, colNum):
        #显示配置文件
        if not hasattr(treeItem, 'fpath'):
            return
        text = treeItem.text(colNum)
        fpath = treeItem.fpath
        fname = treeItem.fname
        self.textBrowser.append('打开 ' + text)
        if fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.csv'):
            progressBar = QtWidgets.QProgressBar(self)
            self.statusBar().addWidget(progressBar)
            #定义数据模型
            model = myWidgets.Model(fpath)
            model.progressBarRangeSignal.connect(progressBar.setRange)
            model.progressBarValueSignal.connect(progressBar.setValue)
            model.progressBarDelSignal.connect(progressBar.deleteLater)
            model.itemChanged.connect(self.tabWidget.changeTabTitle)
            model.savedSignal.connect(self.tabWidget.setPrimaryTabTitle)
            model.setData()
            #定义表格呈现数据
            table = myWidgets.TableView(model, self)
            self.tabWidget.addTab(table, fname)
            self.tabWidget.setCurrentWidget(table)
            self.tabWidget.parentWidget().setWindowTitle(fpath)
        elif fname.endswith('.txt'):
            #读取文本文件
            progressBar = QtWidgets.QProgressBar(self)
            self.statusBar().addWidget(progressBar)
            #文本编辑器
            textEdit = myWidgets.TextEdit(fpath, self)
            textEdit.textChanged.connect(self.tabWidget.changeCurentTabTiltle)
            textEdit.textSignal.connect(self.textBrowser.append)
            textEdit.savedSignal.connect(self.tabWidget.setPrimaryTabTitle)
            textEdit.progressBarRangeSignal.connect(progressBar.setRange)
            textEdit.progressBarValueSignal.connect(progressBar.setValue)
            textEdit.progressBarDelSignal.connect(progressBar.deleteLater)
            textEdit.setData()
            self.tabWidget.addTab(textEdit, fname)
            self.tabWidget.setCurrentWidget(textEdit)
            self.tabWidget.parentWidget().setWindowTitle(fpath)
        else:
            message = QtWidgets.QMessageBox(self)
            message.setWindowTitle(u'文件读取出错')
            message.setText(u'不支持打开该文件！')
            message.show()

    def showColumns(self, colInfo):
        print('showColumns')
        #显示要处理的列名
        if not self.hasDockRight:
            #如果还没有dockRight就创建一个
            self.dockRight.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
            self.dockRight.setWindowTitle(u'选择待处理的列名')
            self.dockRight.setMaximumWidth(320)
            #创建显示列名的表格
            self.colTable = myWidgets.ColTable(self)
            self.colTable.textSignal.connect(self.textBrowser.append)
            self.colTable.showColumnSignal.connect(self.tabWidget.showColumnInWorkWidget)
            self.colTable.setColumnCount(3)
            self.colTable.setRowCount(20)
            headerItem1 = QtWidgets.QTableWidgetItem(u'列名')
            headerItem2 = QtWidgets.QTableWidgetItem(u'位置')
            headerItem3 = QtWidgets.QTableWidgetItem(u'选择')
            self.colTable.setHorizontalHeaderItem(0, headerItem1)
            self.colTable.setHorizontalHeaderItem(1, headerItem2)
            self.colTable.setHorizontalHeaderItem(2, headerItem3)
            self.colTable.horizontalHeader().setFixedHeight(25)
            self.colTable.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:skyblue;color: black;border: 1px solid #6c6c6c;}")
            self.dockRight.setWidget(self.colTable)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockRight, QtCore.Qt.Horizontal)
            self.hasDockRight = True
        self.colTable.appendRow(colInfo)

    def startWork(self):
        #开始匹配
        if self.colTable is None:
            message = QtWidgets.QMessageBox(self)
            message.setWindowTitle(u'任务出错')
            message.setText(u'请选择任务表和要处理的列！')
            message.show()
            return
        cols = []
        colAmount = self.colTable.length
        for i in range(colAmount):
            item = self.colTable.item(i, 0)
            widget = self.colTable.cellWidget(i, 2)
            if widget.checkState() == QtCore.Qt.Checked:
                cols.append(item.text())
        if not cols:
            message = QtWidgets.QMessageBox(self)
            message.setWindowTitle(u'任务出错')
            message.setText(u'不存在要处理的列！')
            message.show()
            return
        #启动后台进程
        self.mainWorker.resultFinishedSignal.connect(self.tabWidget.workWidget.showResult)
        dataPath = self.tabWidget.workWidget.fpath
        self.mainWorker.setConf(dataPath, cols)
        self.mainWorker.start()
        self.textBrowser.append('后台ICD编码开始！')

class TableWidget(QtWidgets.QTableWidget):
    
    dataReadySignal = QtCore.pyqtSignal(pd.DataFrame)
    progressBarRangeSignal = QtCore.pyqtSignal(int, int)
    progressBarValueSignal = QtCore.pyqtSignal(int)
    progressBarDelSignal = QtCore.pyqtSignal()
    
    def __init__(self, fp, parent = None):
        super(TableWidget, self).__init__(parent)
        self.fp = fp
        self.dataReadySignal.connect(self.showData)
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.openFile)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.initPopMenu()
    
    def __del__(self):
        self.thread.quit()
        print('__del__', self.thread.isRunning())
        
    def openFile(self):
        df = File(self.fp).Read()
        self.progressBarRangeSignal.emit(0, len(df) * len(df.columns))
        self.dataReadySignal.emit(df)
    
    @QtCore.pyqtSlot(pd.DataFrame)
    def showData(self, df):
        print('showData')
        cols = list(df.columns)
        data = df.values

        self.setRowCount(len(data) + 10)
        self.setColumnCount(len(cols) + 10)
        self.setHorizontalHeaderLabels(cols)
        
        t = time.time()
        for i in range(len(data)):
            for j in range(len(cols)):
                self.progressBarValueSignal.emit(len(cols) * i + j + 1)
                if data[i][j] == np.nan:
                    continue
                if type(data[i][j]) == float:#判断df缺失值
                    continue
                val = str(data[i][j]).encode('utf8').decode('utf8')
                #item = QtWidgets.QTableWidgetItem(val)
                self.setItem(i, j, QtWidgets.QTableWidgetItem(val))
        self.progressBarDelSignal.emit()
        print(time.time() - t)
        
    def initPopMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        a = QtWidgets.QAction('添加到处理列', self)
        b = QtWidgets.QAction('从处理列删除', self)
        self.popMenu.addAction(a)
        self.popMenu.addAction(b)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
    
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()

def main():
    
    app = QtWidgets.QApplication([])
    
    mainWorker = myWidgets.MainWorker()
    mainWindow = MainWindow(mainWorker)
    mainWindow.show()
    
    app.exec_()

if __name__ == "__main__":
     
    main()






























