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

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu,self).__init__()
        self.resize(926, 651)
        self.setWindowTitle("医疗诊断数据清洗与自动编码")
        self.initToolBar()
        self.initMenuBar()
        self.initTree()
        self.initTable()
        self.initPlainTextEdit()
        self.initDockWidget()
    def initLabel(self):
        self.label = QtWidgets.QLabel(self.toolbar)
        self.label.setGeometry(QtCore.QRect(150, 0, 120, 33))
        self.label.setText("请选择需要清洗的列：")
    def initComboBox(self):
        self.ComboBox=QComboBox(self.toolbar)
        self.ComboBox.insertItem(0,self.tr("ZYZD"))
        self.ComboBox.insertItem(1,self.tr("QTZD1"))
        self.ComboBox.insertItem(1,self.tr("QTZD2"))
        self.ComboBox.insertItem(1,self.tr("QTZD3"))
        self.ComboBox.insertItem(1,self.tr("QTZD4"))
        self.ComboBox.setGeometry(QtCore.QRect(280, 0, 80, 33))
    def initPlainTextEdit(self):
        self.plainTextEdit_output = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit_output.setGeometry(QtCore.QRect(0, 556, 926, 96))
    def initTree(self):
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["文件列表"])
        self.tree.setGeometry(QtCore.QRect(0, 56, 150, 500))

        root= QTreeWidgetItem(self.tree)
        root1= QTreeWidgetItem(self.tree)
        root2= QTreeWidgetItem(self.tree)
        root3= QTreeWidgetItem(self.tree)

        root.setText(0,'标准文件')
        root1.setText(0,'待清洗文件')
        root2.setText(0,'自定义分词词典')
        root3.setText(0,'替换词表')
        child1 = QTreeWidgetItem(root)  
        child1.setText(0,'child1')  
        child2 = QTreeWidgetItem(root1)  
        child2.setText(0,'child2')  
        child3 = QTreeWidgetItem(root2)  
        child3.setText(0,'child3')
        child4 = QTreeWidgetItem(root3)  
        child4.setText(0,'child4')  
        self.tree.addTopLevelItem(root)
        self.tree.addTopLevelItem(root1) 
        self.tree.addTopLevelItem(root2)
        self.tree.addTopLevelItem(root3)
    def initTable(self):
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(150, 56, 776, 500))
        self.tab_1 = QtWidgets.QWidget()
        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 770, 473))
        self.tableWidget.setColumnCount(20)
        self.tableWidget.setRowCount(20)
        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.addTab(self.tab_1, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), "卫计委标准数据")
    def initToolBar(self):
        #初始化工具栏
        self.toolbar = QToolBar(self)
        
        #打开文件工具
        actOfTool1 = QAction(self)
        actOfTool1.setIcon(QIcon('./source/7.png'))
        actOfTool1.setToolTip('Open file (CTRL+O)')
        actOfTool1.setShortcut('CTRL+O')

        #保存文件工具
        actOfTool2 = QAction(self)
        actOfTool2.setIcon(QIcon('./source/6.png'))
        actOfTool2.setToolTip('Save file (CTRL+S)')
        actOfTool2.setShortcut('CTRL+S')

        #查找文件工具
        actOfTool3 = QAction(self)
        actOfTool3.setIcon(QIcon('./source/3.png'))
        actOfTool3.setToolTip('search file (CTRL+S)')
        actOfTool3.setShortcut('CTRL+F')

        #查找执行工具
        actOfTool4 = QAction(self)
        actOfTool4.setIcon(QIcon('./source/9.png'))
        actOfTool4.setToolTip('Save file (CTRL+S)')
        actOfTool4.setShortcut('CTRL+F')

        #添加工具
        self.toolbar.addAction(actOfTool1)
        self.toolbar.addAction(actOfTool2)
        self.toolbar.addAction(actOfTool3)
        self.toolbar.addAction(actOfTool4)
        self.addToolBar(self.toolbar)
    def initMenuBar(self):
        #初始化菜单栏
        menubar = self.menuBar()
        
        #文件菜单
        act1 = QAction('导入标准卫计委文件', self)
        act1.setShortcut('CTRL+W')
        act2 = QAction('导入待清洗文件', self)
        act2.setShortcut('CTRL+Q')
        act3 = QAction('导入用户词典', self)
        act4 = QAction('导入替换词表', self)
        fileMenu = menubar.addMenu('文件') 
        fileMenu.addAction(act1)
        fileMenu.addAction(act2)
        fileMenu.addAction(act3)
        fileMenu.addAction(act4)
        #保存菜单
        act5 = QAction('保存', self)
        act5.setShortcut('CTRL+S')
        act6 = QAction('全部保存', self)
        act6.setShortcut('CTRL+SHIFT+S')
        save_menu = menubar.addMenu('保存')
        save_menu.addAction(act5)
        save_menu.addAction(act6)
        #设置菜单
        act7 = QAction('字体', self)
        setting_menu = menubar.addMenu('设置')
        setting_menu.addAction(act7)

        #关于菜单
        act8 = QAction('软件使用说明', self)
        act9 = QAction('关于我们...', self)
        setting_menu = menubar.addMenu('关于')
        setting_menu.addAction(act8)
        setting_menu.addAction(act9)

    def initDockWidget(self):
        #初始化dockWidget
        ############设置dockLeft
        dockLeft = QDockWidget(self)
        dockLeft.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockLeft)
        dockLeft.setWidget(self.tree)
        dockLeft.setMinimumWidth(200)
        #dockLeft.setFixedWidth(150)
        #dockLeft.setMaximumWidth(250)
        #dockLeft.setDockNestingEnabled(True);
        ############设置dockRight
        dockRight = QDockWidget(self)
        dockRight.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockRight)
        dockRight.setWidget(self.tabWidget)
        dockRight.setWidget(self.tableWidget)

        dockBottom = QDockWidget(self)
        dockBottom.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dockBottom)
        dockBottom.setWidget(self.plainTextEdit_output)
        dockBottom.setMaximumHeight(100)

if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    mainmenu = MainMenu()
    mainmenu.show()
    app.exec_()