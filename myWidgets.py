import os
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from file import File, Format
import ICD

class ConfTreeItem(QtWidgets.QTreeWidgetItem):
    
    def __init__(self, fname, parent = None):
        super(ConfTreeItem, self).__init__(parent)
        #添加成员
        self.fname = fname
        self.fpath = os.getcwd() + '\\data\\' + fname
        self.conf = {'stdICD-10.csv':'标准ICD-10' \
                     , 'swap.xlsx':'替换词表'  \
                     , 'del.txt':'删除词表' \
                     , 'dd.txt':'分词词典' }
    
    def addTreeItem(self, child):
        #添加此树的子元素
        self.addChild(child)
        self.childs.append(child)
        
    def isAddChild(self, fname):
        #判断是否能添加text的子元素
        for child in self.childs:
            text = child.text(0)
            if text in self.conf:
                break

class UserTreeItem(QtWidgets.QTreeWidgetItem):
    
    def __init__(self, parent = None):
        super(UserTreeItem, self).__init__(parent)
        #添加成员
        self.childs = []
    def addTreeItem(self, child):
        #添加此树的子元素
        self.childs.append(child)
        
    def isAddChild(self, fname):
        #判断是否能添加text的子元素
        for child in self.childs:
            text = child.text(0)
            if text == fname:
                return
        treeItem = QtWidgets.QTreeWidgetItem(self)
        treeItem.setText(0, fname)
        self.addTreeItem(treeItem)
        self.setExpanded(True)
        
class TreeItem(QtWidgets.QTreeWidget):
    def __init__(self, parent = None):
        super(TreeItem, self).__init__(parent)
        # 添加成员
    
    def mousePressEvent(self, e):
        if QtCore.Qt.LeftButton == e.button():
            pass

class HeaderItem(QtGui.QStandardItem):
    def __init__(self, text, parent = None):
        super(HeaderItem, self).__init__(parent)
        # 添加成员
        self.setText(text)

class Model(QtGui.QStandardItemModel):
    #定义发送给进度条的信号
    progressBarRangeSignal = QtCore.pyqtSignal(int, int)
    progressBarValueSignal = QtCore.pyqtSignal(int)
    progressBarDelSignal = QtCore.pyqtSignal()
    setHeaderSignal = QtCore.pyqtSignal(list)
    savedSignal = QtCore.pyqtSignal()
    
    def __init__(self, fpath, parent = None):
        super(Model, self).__init__(parent)
        # 添加成员
        self.fpath = fpath
        self.isChanged = False
        
    def setData(self):
        #设置表格的数据
        df = File(self.fpath).Read()
        cols = list(df.columns)
        data = df.values
        self.progressBarRangeSignal.emit(0, len(df) * len(df.columns))
        #设置表格列数，行数，列名
        self.setRowCount(len(data) + 1)
        self.setColumnCount(len(cols) + 1)
        #self.setHorizontalHeaderLabels(cols)
        for i in range(len(cols)):
            #header = QtGui.QStandardItem(cols[i])
            header = HeaderItem(str(cols[i]))
            header.setEditable(False)
            header.setSelectable(True)
            header.setEnabled(True)
            header.setFlags(QtCore.Qt.ItemIsSelectable)
            header.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setHorizontalHeaderItem(i, header)
        
        for i in range(len(data)):
            for j in range(len(cols)):
                self.progressBarValueSignal.emit(len(cols) * i + j + 1)
                if data[i][j] == np.nan:
                    continue
                if type(data[i][j]) == float:#判断df缺失值
                    continue
                val = str(data[i][j]).encode('utf8').decode('utf8')
                item = QtGui.QStandardItem(val)
                self.setItem(i, j, item)
        self.progressBarDelSignal.emit()
    
    def save(self):
        if not self.isChanged:
            return
        pass

class TableView(QtWidgets.QTableView):
    
    textSignal = QtCore.pyqtSignal(str)
    def __init__(self, model, parent = None):
        super(TableView, self).__init__(parent)
        # 添加成员
        self.fpath = model.fpath
        self.model = model
        self.isChanged = False
        #初始化
        self.setModel(model)
        self.initPopMenu()
        self.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:skyblue;color: black;border: 1px solid #6c6c6c;}")
    
    def initPopMenu(self):
        #设置鼠标点击的菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        act1 = QtWidgets.QAction(u'&保存', self)
        act1.setToolTip('Save file (CTRL+S)')
        act1.setShortcut('CTRL+S')
        act1.triggered.connect(self.model.save)
        act2 = QtWidgets.QAction(u'&清空', self)
        act2.setToolTip('clear (CTRL+ALT+C)')
        act2.setShortcut('CTRL+ALT+C')
        act2.triggered.connect(self.clearMessage)
        self.popMenu.addAction(act1)
        self.popMenu.addAction(act2)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
        #在鼠标右击的位置显示菜单
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()
    
    def clearMessage(self):
         result = QtWidgets.QMessageBox.question (self, u'是否清空?', \
                  u'确定要把当前所有内容清空吗！', \
                  buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  defaultButton = QtWidgets.QMessageBox.No)
         if result == QtWidgets.QMessageBox.Yes:
             self.model.clear()

class TextEdit(QtWidgets.QTextEdit):
    #定义发送给进度条的信号
    progressBarRangeSignal = QtCore.pyqtSignal(int, int)
    progressBarValueSignal = QtCore.pyqtSignal(int)
    progressBarDelSignal = QtCore.pyqtSignal()
    textSignal = QtCore.pyqtSignal(str)
    savedSignal = QtCore.pyqtSignal()
    
    def __init__(self, fpath, parent = None):
        super(TextEdit, self).__init__(parent)
        # 添加成员
        self.isChanged = False
        self.fpath = fpath
        #初始化
        self.initPopMenu()
        
    def setData(self):
        datas = File(self.fpath).Read()
        print(len(datas))
        text = ''
        self.progressBarRangeSignal.emit(0, len(datas))
        for i in range(len(datas)):
            text = text + datas[i]
            self.progressBarValueSignal.emit(i)
        self.setPlainText(text)
        self.progressBarDelSignal.emit()
            
    def initPopMenu(self):
        #设置鼠标点击的菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        act1 = QtWidgets.QAction(u'&保存', self)
        act1.setToolTip('Save file (CTRL+S)')
        act1.setShortcut('CTRL+S')
        act1.triggered.connect(self.save)
        act2 = QtWidgets.QAction(u'&清空', self)
        act2.setToolTip('clear (CTRL+ALT+C)')
        act2.setShortcut('CTRL+ALT+C')
        act2.triggered.connect(self.clearMessage)
        self.popMenu.addAction(act1)
        self.popMenu.addAction(act2)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
        #在鼠标右击的位置显示菜单
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()
        
    def save(self):
        #保存内容
        if not self.isChanged:
            return
        text = self.toPlainText()
        try:
            f = open(self.fpath, mode = 'w', encoding = 'utf-8')
            f.write(text)
            self.textSignal.emit(u'保存文本成功！')
            self.savedSignal.emit()
        except:
            message = QtWidgets.QMessageBox(self)
            message.setWindowTitle(u'出错')
            message.setText(u'保存文件失败!')
            message.show()
        finally:
            f.close()
        
    def clearMessage(self):
         result = QtWidgets.QMessageBox.question (self, u'是否清空?', \
                  u'确定要把当前所有内容清空吗！', \
                  buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  defaultButton = QtWidgets.QMessageBox.No)
         if result == QtWidgets.QMessageBox.Yes:
             self.clear()
         
class LoadWorker(QtCore.QThread):
    #读取不同类型的文件发送不同信号
    txtSignal = QtCore.pyqtSignal(list)
    dfSignal = QtCore.pyqtSignal(pd.DataFrame)
    loadErrorSignal = QtCore.pyqtSignal()
    
    def __init__(self, fpath, parent = None):
        super(LoadWorker, self).__init__(parent)
        self.fpath = fpath
        
    def run(self):
        #重载run函数
        reader = File(self.fpath)
        if reader.format == Format.csv:
            #读取csv文件
            data = reader.Read()
            self.dfSignal.emit(data)
        elif reader.format == Format.excel:
            #读取Excel文件
            data = reader.Read()
            self.dfSignal.emit(data)
        elif reader.format == Format.txt:
            #读取txt文件
            data = reader.Read()
            self.txtSignal.emit(data)
        else:
            #其他情况
            self.loadErrorSignal.emit()
                
class HeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent = None):
        super(HeaderItem, self).__init__(parent)
        self.initPopMenu()

    def initPopMenu(self):
        #设置鼠标点击的菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        a = QtWidgets.QAction('保存', self)
        b = QtWidgets.QAction('保存全部', self)
        self.popMenu.addAction(a)
        self.popMenu.addAction(b)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
        #在鼠标右击的位置显示菜单
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()
        
class TabWidget(QtWidgets.QTabWidget):
    
    textSignal = QtCore.pyqtSignal(str)
    addTreeSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        # 添加成员
        self.workWidget = None
        # 初始化
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)
        
    def addedWidget(self, fname):
        #当读取一个表格文件时给发送信号
        self.addTreeSignal.emit(fname)
    
    def showColumnInWorkWidget(self, localtion):
        #在主要任务表里显示指定列
        self.textSignal.emit(u'在主要任务表里显示第 {0} 列'.format(localtion))
        self.setCurrentWidget(self.workWidget)
        self.workWidget.selectColumn(localtion)
        
    def setWorkWidget(self):
        #设置主要工作的控件
        result = QtWidgets.QMessageBox.question (self, u'设置主要任务', \
                  u'确定要把当前表格设置\n成主要处理任务吗！', \
                  buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  defaultButton = QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            w = self.currentWidget()
            w.act1.setEnabled(True)
            w.act2.setEnabled(False)
            self.workWidget  = w
            self.textSignal.emit(u'把 ' + self.currentWidget().fpath.split('/')[-1] + u' 为主要任务表。')
    
    def closeTab(self, index):
        w = self.widget(index)
        if not w.isChanged:
            self.removeTab(index)
            return
        result = QtWidgets.QMessageBox.question (self, u'设置主要任务', \
                  u'确定要把当前表格设置\n成主要处理任务吗！', \
                  buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  defaultButton = QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.removeTab(index)
    
    def changeCurentTabTiltle(self):
        #改变当前tab的标题
        w = self.currentWidget()
        index = self.currentIndex()
        if not hasattr(w, 'fpath'):
            return
        if '/' in w.fpath:
            title = w.fpath.split('/')[-1] + '*'
        else:
            title = w.fpath.split('\\')[-1] + '*'
        self.setTabText(index, title)
        w.isChanged = True
    
    def changeTabTitle(self, item):
        w = self.currentWidget()
        index = self.currentIndex()
        if not hasattr(w, 'fpath'):
            return
        if '/' in w.fpath:
            title = w.fpath.split('/')[-1] + '*'
        else:
            title = w.fpath.split('\\')[-1] + '*'
        self.setTabText(index, title)
        if hasattr(w, 'isChanged'):
            w.isChanged = True
        else:
            if hasattr(w, 'model'):
                w.model.isChanged = True
    
    def setPrimaryTabTitle(self):
        w = self.currentWidget()
        index = self.currentIndex()
        if not hasattr(w, 'fpath'):
            return
        if '/' in w.fpath:
            title = w.fpath.split('/')[-1]
        else:
            title = w.fpath.split('\\')[-1]
        self.setTabText(index, title)
        if hasattr(w, 'isChanged'):
            w.isChanged = False
        else:
            if hasattr(w, 'model'):
                w.model.isChanged = False

class ColTable(QtWidgets.QTableWidget):
    
    textSignal = QtCore.pyqtSignal(str)
    showColumnSignal = QtCore.pyqtSignal(int)
    
    def __init__(self, parent = None):
        super(ColTable, self).__init__(parent)
        self.length = 0
        self.initPopMenu()
        
    def appendRow(self, colInfo):
        #添加一行
        if self.existColName(colInfo[0]):
            return
        currentRowCount = self.rowCount()
        self.setRowCount(1 + currentRowCount)
        #第一列内容
        item = QtWidgets.QTableWidgetItem(colInfo[0])
        item.setFlags(QtCore.Qt.NoItemFlags)
        item.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
        self.setItem(self.length, 0, item)
        #第二列内容
        localtion = QtWidgets.QTableWidgetItem(str(colInfo[1]))
        self.setItem(self.length, 1, localtion)
        #第三列内容
        checkBox = QtWidgets.QCheckBox(self)
        checkBox.setCheckState(QtCore.Qt.Checked)
        self.setCellWidget(self.length, 2, checkBox)
        self.length += 1
    
    def existColName(self, colName):
        #判断col是否已经存在（选上）
        boo = False
        for i in range(self.length):
            item = self.item(i, 0)
            col = item.text()
            if col == colName:
                boo = True
                break
        return boo
    
    def seekColumn(self):
        #获得选中的行，并发出信号,请求在任务表格里给出该列的位置
        rowIndex =  self.currentRow()
        if rowIndex < 0 or rowIndex >= self.length:
            #如果超出范围
            self.popMessage('选择行错误', '选择的行超出范围')
            return
        val = self.item(rowIndex, 1).text()
        localtion = int(val)
        self.showColumnSignal.emit(localtion)
        self.textSignal.emit(u'在任务表格里给出第 {0} 列的位置'.format(localtion))
        
    def popMessage(self, title, content):
        #弹出提示信息或出错信息
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle(title)
        message.setText(content)
        message.show()
        
    def initPopMenu(self):
        #设置鼠标点击的菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        act1 = QtWidgets.QAction('删除', self)
        act2 = QtWidgets.QAction('显示', self)
        act2.triggered.connect(self.seekColumn)
        self.popMenu.addAction(act1)
        self.popMenu.addAction(act2)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
        #在鼠标右击的位置显示菜单
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()
        
class TableWidget(QtWidgets.QTableWidget):
    
    progressBarRangeSignal = QtCore.pyqtSignal(int, int)
    progressBarValueSignal = QtCore.pyqtSignal(int)
    progressBarDelSignal = QtCore.pyqtSignal()
    columnSignal = QtCore.pyqtSignal(list)
    mainWorkSetSignal = QtCore.pyqtSignal()
    textSignal = QtCore.pyqtSignal(str)
    savedSignal = QtCore.pyqtSignal()
    
    def __init__(self, fp, parent = None):
        super(TableWidget, self).__init__(parent)
        self.isMainWork = False
        self.isChanged = False
        self.fpath = fp
        self.showData()
        self.initPopMenu()
        self.horizontalHeader().setFixedHeight(25)
        self.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:skyblue;color: black;border: 1px solid #6c6c6c;}")

    def showData(self):
        print('showData')
        df = File(self.fpath).Read()
        cols = list(df.columns)
        data = df.values
        self.progressBarRangeSignal.emit(0, len(data) * len(cols))
        
        self.setRowCount(len(data) + 5)
        self.setColumnCount(len(cols) + 5)
        #self.setHorizontalHeaderLabels(cols)
        for i in range(len(cols)):
            header = QtWidgets.QTableWidgetItem(str(cols[i]))
            self.setHorizontalHeaderItem(i, header)
        
        for i in range(len(data)):
            for j in range(len(cols)):
                self.progressBarValueSignal.emit(len(cols) * i + j + 1)
                if data[i][j] == np.nan:
                    continue
                if type(data[i][j]) == float:#判断df缺失值
                    continue
                val = str(data[i][j]).encode('utf8').decode('utf8')
                item = QtWidgets.QTableWidgetItem(val)
                self.setItem(i, j, item)
        self.progressBarDelSignal.emit()
    
    def showResult(self, result):
        #显示处理结果,result为DataFrame
        print('showResult')
        cols = list(result.columns)
        data = result.values
        columnCount = self.columnCount()
        for i in range(len(cols)):
            #添加lie
            self.insertColumn(columnCount + i)
            header = QtWidgets.QTableWidgetItem(str(cols[i]))
            self.setHorizontalHeaderItem(columnCount + i, header)
        
        for i in range(len(data)):
            for j in range(len(cols)):
                if data[i][j] == np.nan:
                    continue
                if type(data[i][j]) == float:#判断df缺失值
                    continue
                val = str(data[i][j]).encode('utf8').decode('utf8')
                item = QtWidgets.QTableWidgetItem(val)
                self.setItem(i, j + columnCount, item)
        self.popMessage(u'处理完成', u'已经处理完成！')
    
    def selectColName(self):
        #发出信号，请求在ColTable显示列名
        colNum = self.currentColumn()
        item = self.horizontalHeaderItem(colNum)
        if item is None:
            self.popMessage('选择列名出错', '选择的列为空！')
            return
        colName = item.text()
        colInfo = [colName, colNum]
        self.columnSignal.emit(colInfo)
        self.textSignal.emit('添加'+ colName + '到处理列')
    
    def emitMainWork(self):
        #设置自己为主要任务表格
        self.isMainWork = True
        self.mainWorkSetSignal.emit()
    
    def initPopMenu(self):
        #设置鼠标点击的菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.popMenu = QtWidgets.QMenu(self)
        self.act1 = QtWidgets.QAction('添加当前列到处理列', self)
        self.act1.setEnabled(False)
        self.act1.triggered.connect(self.selectColName)
        self.act2 = QtWidgets.QAction('设置为待处理文件', self)
        self.act2.triggered.connect(self.emitMainWork)
        self.act3 = QtWidgets.QAction(u'&保存', self)
        self.act3.setToolTip('Save file (CTRL+S)')
        self.act3.setShortcut('CTRL+S')
        self.act3.triggered.connect(self.save)
        self.popMenu.addAction(self.act2)
        self.popMenu.addAction(self.act1)
        self.popMenu.addAction(self.act3)
        self.customContextMenuRequested.connect(self.showMenu)
        
    def showMenu(self, point):
        #在鼠标右击的位置显示菜单
        self.popMenu.move(QtGui.QCursor.pos())
        self.popMenu.show()

    def popMessage(self, title, content):
        #弹出提示信息或出错信息
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle(title)
        message.setText(content)
        message.show()
    
    def save(self):
        pass

class MainWorker(QtCore.QThread):
    
    resultFinishedSignal = QtCore.pyqtSignal(ICD.pd.DataFrame)
    
    def __init__(self, parent = None):
        super(MainWorker, self).__init__(parent)
        self.fpath = None
        self.cols = None
    
    def setConf(self, fpath, cols):
        self.fpath = fpath
        self.cols = cols
    
    def run(self):
        #重载run方法
        if self.fpath is None or self.cols is None:
            return
        print('run MainWorker')
        queue = ICD.mp.Queue()
        process = ICD.mp.Process(name = 'aICD', target = ICD.main, args = (self.fpath, self.cols, queue))
        process.start()
        process.join()
        result = queue.get()
        self.resultFinishedSignal.emit(result)







