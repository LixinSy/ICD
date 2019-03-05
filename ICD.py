# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:30:36 2017

@author: 李莘
"""

import os, sys, time, copy
import numpy as np
import pandas as pd
import multiprocessing as mp
import jieba
from file import File
#from PyQt5.QtCore import QTread

class Diacrisis:
    
    amount = 0   #诊断的总数量
    dictPath = r'./data/dd.txt' #分词字典
    stdICD_path = r'./data/stdICD-10.csv' #标准ICD表
    replacePath = r'./data/swap.xlsx' #替换词 表
    usedPath = r'./data/used.xlsx' #常用诊断表
    delPath = r'./data/del.txt'  #
    stdICD = None        #标准ICD表
    usedWords = None     #常用诊断表
    replaceWords = None  #替换词 表
    IDFdict = None       #权重表
    record = {}          #
    delChars = None # ' `~!@#$%^&*-_=+(){}[];:<>,.?·~（）【】；：《》，。？、‘’“”并及和与病症的性\'\"\\'
    
#**************************public*************************
    def InitDict():
        #加载自己的字典，调整原来的字典
        if not Diacrisis.dictPath:
            return
        jieba.load_userdict(Diacrisis.dictPath)
        jieba.del_word('伴多')
        jieba.del_word('伴有')
        jieba.del_word('二型')
        jieba.suggest_freq(('伴','多'), tune = True)
        jieba.suggest_freq(('伴','有'), tune = True)
        jieba.suggest_freq(('二','型'), tune = True)
        
    def InitOther():
        #加载删词词库
        Diacrisis.delChars = File(Diacrisis.delPath).Read()
        if not Diacrisis.delChars:
            print('读取失败')
        #加载常用诊断表
        used_df = File(Diacrisis.usedPath).Read()
        print(len(used_df))
        if len(used_df) > 0:
            Diacrisis.usedWords = pd.Series(index = list(used_df['诊断'].values), data = list(used_df['编码'].values))
        #加载换词表
        re_df = File(Diacrisis.replacePath).Read()
        print(len(re_df))
        if len(re_df) > 0:
            Diacrisis.replaceWords = pd.Series(index = list(re_df['ToReplace'].values), data = list(re_df['truly'].values))
        #加载标准ICD表
        Diacrisis.stdICD = File(Diacrisis.stdICD_path).Read()
        print(len(Diacrisis.stdICD))
        Diacrisis.stdICD['std-cut'] = Diacrisis.CleanStdICD(Diacrisis.stdICD['疾病名称'])[1]
        #Diacrisis.stdICD.to_csv(Diacrisis.stdICD_path, encoding = 'utf8', index = False)
        #加载权重表
        Diacrisis.Idf()
        
    def UpdateOther():
        #
        pass
        
    def CleanStdICD(series):
        #给一列数据的所有字符串分词
        List1 = []
        List2 = []
        #series = series.fillna('')
        List = series.values
        for x in List:
            if not x:
                List1.append('')
                List2.append([])
                continue
            strList = jieba.lcut(str(x))
            strList = Diacrisis.Rejust(strList)
            List2.append(strList)
            string = ','.join(strList)
            List1.append(string)
        return (List1, List2)
     
    def Rejust(aList):
        #aList是分词后的列表，转换某些词的意思或删除某些词语
        if not aList:
            return
        newList = []
        n = len(aList)
        for i in range(n):
            if aList[i] in Diacrisis.replaceWords:
                aList[i] = str(Diacrisis.replaceWords[aList[i]])
            elif aList[i] in Diacrisis.delChars:
                continue
            newList.append(aList[i])
        List = list(set(newList))
        List.sort(key = newList.index)
        return List
          
    def Idf():
        #计算各个string在stdICD中的权值
        lines = Diacrisis.stdICD['std-cut'].values
        d = dict()
        n = 0
        for line in lines:
            if not line:
                continue
            n += 1
            for word in line:
                if not word:
                    continue
                if type(word) != str:
                    word = str(word)
                if word not in d:
                    d[word] = 1
                else:
                    d[word] += 1
        for word in d:
            d[word] = np.log10(n/d[word])
        print('共有{}个词有权值'.format(len(d)))
        Diacrisis.IDFdict = d
        
        f = open(r'./data/idf.txt', 'w')
        for i in d:
            f.write(str(i) + '\t' + str(d[i]) + '\n')
        f.close()
            
    def RecordInfo():
        #显示处理的数据中多次出现的诊断
        if len(Diacrisis.record) <= 0:
            print('没有发现多次出现的诊断！')
            return
        for w in Diacrisis.record:
            print(w, Diacrisis.record[w])
            
            if w not in Diacrisis.usedWords and Diacrisis.record[w][0] >= 5:
                Diacrisis.usedWords[w] = Diacrisis.record[w][1]
        data = {'诊断' : Diacrisis.usedWords.keys(), '编码' : Diacrisis.usedWords.values}
        df = pd.DataFrame(data)
        df.to_excel(Diacrisis.usedPath, index = False, encoding = 'utf8')
    
    #**************************private*************************
    def __init__(self, name, col, n):
        if type(name) != str:
            name = str(name)
        self.pathema = name
        if name in Diacrisis.record:
            self.pos.append((col, n))
            self.count += 1
            Diacrisis.record[name][0] += 1
        else:
            self.pos = [(col, n)]
            self.count = 1
            Diacrisis.record[name] = [1, None]
    
    def CutName(self):
        #分词并清洗
        newList = []
        List = jieba.lcut(self.pathema)
        for word in List:
            if word in Diacrisis.delChars:
                continue
            elif word in Diacrisis.replaceWords:
                newList.append(str(Diacrisis.replaceWords[word]))
                continue
            newList.append(word)
        myList = list(set(newList))
        myList.sort(key = newList.index)
        self.words = myList
    
    def SimilarRate(self, bList):
        #余弦相似度法计算字符串相似度,前提是已经有IDF权值表
        if not Diacrisis.IDFdict:
            print('还没有IDF权值表！')
            return
        if not self.words or not bList:
            return 0
        if type(bList) != list:
            print('类型错误！')
            return
        aVector = []
        bVector = []
        List = list(set(self.words + bList))
        for word in List:
            if not word:
                continue
            if word not in Diacrisis.IDFdict:
                continue
            x = Diacrisis.IDFdict[word]
            if word in self.words:
                aVector.append(x)
            else:
                aVector.append(0)
                
            if word in bList:
                bVector.append(x)
            else:
                bVector.append(0)
        aVector = np.array(aVector)
        bVector = np.array(bVector)
        aMagnitude = np.sqrt(np.dot(aVector, aVector))
        bMagnitude = np.sqrt(np.dot(bVector, bVector))
        if not aMagnitude or not bMagnitude:
            return 0.0
        rate = np.dot(aVector, bVector) / (aMagnitude * bMagnitude)
        return rate
    
    def FiltrateLines(self, inter = False):
        #在stdICD中筛选出和objList相关的字符串
        if not self.words:
            return
        table = []
        n = len(Diacrisis.stdICD)
        for i in range(n):
            for word in Diacrisis.stdICD['std-cut'][i]:
                if word in self.words:
                    if word in ['型','伴','有']:
                        continue
                    if inter:
                        table.append( [ Diacrisis.stdICD['std-cut'][i],\
                                        Diacrisis.stdICD['主要编码'][i],\
                                        Diacrisis.stdICD['疾病名称'][i] ] )
                    else:
                        table.append( [ Diacrisis.stdICD['std-cut'][i],\
                                        Diacrisis.stdICD['主要编码'][i] ] )
                    break
        return table
    
    def Match(self):
        #用余弦相似度查找最佳匹配目标，stdLines-> [ ['std-cut'],['主要编码'] ]
        self.CutName()        
        name = ''.join(self.words)
        max_rate = 0
        stdLines = self.FiltrateLines(inter = False)
        for i in range(len(stdLines)):
            line = stdLines[i]
            std_name = ''.join(line[0])
            if std_name == name:
                max_rate = 1
                ICD = str(line[1])
                break
            
            rate = self.SimilarRate(line[0])
            if rate == 1.0:
                max_rate = 1
                ICD = str(line[1])
                break
            elif max_rate < rate:
                max_rate = rate
                ICD = line[1]
        if max_rate == 0:
            self.newICD = ''
        elif max_rate == 1:
            self.newICD = ICD[:7]
        else:
            self.newICD = ICD[:7]
        #记录已经处理过的诊断，作为记忆，省略之后相同的匹配、更新常用诊断表
        if not Diacrisis.record[self.pathema][1]:
            Diacrisis.record[self.pathema][1] = self.newICD
                
            
    def Find(self):
        #给诊断编码
        if Diacrisis.usedWords is None:
            print('没有常用表！')
            return
        #先在常用诊断表查找
        if self.pathema in Diacrisis.usedWords:
            self.newICD = Diacrisis.usedWords[self.pathema]
            return
        #在记录表中查找
        if Diacrisis.record[self.pathema][1] is not None:
            self.newICD = Diacrisis.record[self.pathema][1]
            return
        #通过余弦算法匹配
        self.Match()
        
#********************************       主要方法         ****************************************
def wordRate(aStr = None, bStr = None):
    #aList和bList是字符串的列表，计算两者的相似度
    if not aStr or not bStr:
        return 0
    List = list(set(aStr + bStr))
    str_count = len(List)
    n = 0
    for s in aStr:
        if s in bStr:
            n = n + 1
    return n / str_count

def similarRate(aList, bList, IDFdict):
    #余弦相似度法计算字符串相似度
    if not aList or not bList:
        return 0
    aVector = []
    bVector = []
    List = list(set(aList + bList))
    for word in List:
        if not word:
            continue
        if word not in IDFdict:
            continue
        #x = IDFdict[word]
        x = round(IDFdict[word], 2)
        if word in aList:
            aVector.append(x)
        else:
            aVector.append(0)
            
        if word in bList:
            bVector.append(x)
        else:
            bVector.append(0)
            
    aVector = np.array(aVector)
    bVector = np.array(bVector)
    aMagnitude = np.sqrt(np.dot(aVector, aVector))
    bMagnitude = np.sqrt(np.dot(bVector, bVector))
    if not aMagnitude or not bMagnitude:
        return 0
    rate = np.dot(aVector, bVector) / (aMagnitude * bMagnitude)
    return rate

def cutName(name, delChars, replaceWords):
    #分词并清洗
    newList = []
    List = jieba.lcut(str(name))
    for word in List:
        if word in delChars:
            continue
        elif word in replaceWords:
            newList.append(str(replaceWords[word]))
            continue
        newList.append(word)
    myList = list(set(newList))
    myList.sort(key = newList.index)
    return myList

def relevantLines(objList, stdICD):
    #在stdICD中筛选出和objList相关的字符串
    if not objList:
        return
    table = []
    n = len(stdICD)
    for i in range(n):
        for word in stdICD['std-cut'][i]:
            if word in objList:
                if word in ['型','伴','有']:
                    continue
                #yield (stdICD['std-cut'][i], stdICD['主要编码'][i])
                table.append( (stdICD['std-cut'][i], stdICD['主要编码'][i]) )
    return table

def match(data, queue, stdICD, IDFdict):
    #给数据ICD编码
    result = []
    for words in data:
        #如果为空值
        if not words:
            result.append('')
            continue

        #主要处理过程
        likelyLines = []
        max_rate = 0
        stdLines = relevantLines(words, stdICD)
        #余弦相似度计算相似度
        for line in stdLines:
            stdCut = line[0]
            #如果字符串一样
            if ''.join(stdCut) == ''.join(words):
                max_rate = 1
                ICD = line[1]
                break
            rate = similarRate(words, stdCut, IDFdict)
            if rate == 0:
                continue
            if rate == 1:
                max_rate = 1
                ICD = line[1]
                break
            elif rate > max_rate:
                max_rate = rate
                ICD = line[1]

                likelyLines = []
                likelyLines.append(line)
            elif rate == max_rate:
                likelyLines.append(line)

        if max_rate == 1:
            result.append(ICD[:7])
        elif max_rate == 0:
            result.append('')
        else:
            if len(likelyLines) <= 1:
                result.append(ICD[:7])
            else:
                #集合法计算相似度
                max_rate = 0
                for line in likelyLines:
                    rate = wordRate(''.join(words), ''.join(line[0]))
                    if rate > max_rate:
                        max_rate = rate
                        ICD = line[1]
                result.append(str(ICD[:7]))

    queue.put(result)
    print(os.getpid())
                
#*****************************************    main      ****************************************
def filterWord(words, delChars, replaceWords):
    #给分词后的words去词，换词
    newList = []
    for word in words:
        if word in delChars:
            continue
        elif word in replaceWords:
            newList.append(str(replaceWords[word]))
            continue
        newList.append(word)
    myList = list(set(newList))
    myList.sort(key = newList.index)
    return myList

def cutLine(arr, delChars, replaceWords):
    #arr为df[''].values, 分词
    strs = []
    List = []
    for name in arr:
        if not name:
            List.append([])
            strs.append('')
            continue
        if type(name) != str:
            List.append([])
            strs.append('')
            continue
        strList = jieba.lcut(name)
        strList = filterWord(strList, delChars, replaceWords)
        List.append(strList)
        strs.append(','.join(strList))
    return (List, strs)

def cleanData(dataDf, cols):
    #一列一列来处理， 一列用CPU核的数量个进程来处理
    if not cols:
        return
    
    processCount = os.cpu_count() 
    total = len(dataDf)
    dataCount = int(round(total / processCount))
    for col in cols:
        processList = []
        queueList = []
        result = []
        #给df[col]分词
        tm = time.time()
        datas = cutLine(dataDf[col].values, Diacrisis.delChars, Diacrisis.replaceWords)[0]
        dataDf[col + '-cut'] = cutLine(dataDf[col].values, Diacrisis.delChars, Diacrisis.replaceWords)[1]
        print(time.time() - tm)
        #创建processCount个进程，并分配数据任务
        for i in range(processCount):
            x = i * dataCount
            y = (i+1) * dataCount
            if (i+1) == processCount:
                x = i * dataCount
                y = total
            data = datas[x:y]
            queue = mp.Queue()
            queueList.append(queue)
            process = mp.Process(target = match, args = (data, queue, Diacrisis.stdICD, Diacrisis.IDFdict ))
            processList.append(process)
            
         #启动进程    
        for i in range(processCount):
            processList[i].start()
        
        #归并进程
        for i in range(processCount):
            processList[i].join()
        
        #获取结果
        for i in range(processCount):
            result = result + queueList[i].get()
            
        dataDf[col + '-result'] = result
        print(col + 'is OK')

def mainWork(dataPath, cols, queue):
    #主函数
    '''
    #dataPath = r'./data/t2dm-utf8.csv'
    dataPath = r'./data/t2dmtest.csv'
    #cols = ['ZYZD','QTZD1','QTZD2','QTZD3','QTZD4','QTZD5','QTZD6','QTZD7','QTZD8','QTZD9','QTZD10','QTZD11','QTZD12','QTZD13','QTZD14','QTZD15']
    colss = ['RYZD']
    '''
    print('mainWork',dataPath, cols)
    df = File(dataPath).Read()
    df.fillna('')
    
    Diacrisis.InitDict()
    Diacrisis.InitOther()
    
    cleanData(df, cols)

    #df.to_csv(r'./data/t2dmutf8-test.csv', index = False, encoding = 'utf-8')
    newCols = []
    for col in cols:
        newCols.append(col + '-result')
    result = df.loc[:, newCols]
    print(newCols, len(result))
    queue.put(result)

def main(dataPath, cols, queue):
    if __name__ == '__main__':
        t = time.time()
        mainWork(dataPath, cols, queue)
        print(time.time() - t)
         
         
         
         
         
         
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            