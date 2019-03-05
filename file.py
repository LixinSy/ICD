# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 15:50:18 2017

@author: 李莘
"""
import pandas as pd
from enum import Enum

class Format(Enum):
    csv = 'csv'
    excel = 'excel'
    txt = 'text'

class File:

    def __init__(self, fileName):
        if not fileName:
            return
        self.fileName = fileName
        #判断文件类型
        if self.fileName.endswith('.csv'):
            self.format = 'csv'
        elif self.fileName.endswith('.xlsx'):
            self.format = 'excel'
        elif self.fileName.endswith('.xls'):
            self.format = 'excel'
        elif self.fileName.endswith('.txt'):
            self.format = 'text'
     
    def Read(self):
        #根据不同文件格式，用不同方法读取
        r = True
        if self.format == 'csv':
            try:
                data = pd.read_csv(self.fileName, encoding = 'utf-8', skip_blank_lines = False)
                self.encoding = 'utf-8'
            except UnicodeDecodeError:
                try:
                    data = pd.read_csv(self.fileName, encoding = 'gbk', skip_blank_lines = False)
                    self.encoding = 'gbk'
                except:
                    print('FileNotFoundError')
                    r = False
        elif self.format == 'excel':
            try:
                data = pd.read_excel(self.fileName, encoding = 'utf-8', skip_blank_lines = False)
                self.encoding = 'utf-8'
            except UnicodeDecodeError:
                try:
                    data = pd.pd.read_excel(self.fileName, encoding = 'gbk', skip_blank_lines = False)
                    self.encoding = 'gbk'
                except:
                    print('FileNotFoundError')
                    r = False
        elif self.format == 'text':
            try:
                f = open(self.fileName, mode = 'r', encoding = 'utf-8')
                data = f.readlines()
                self.encoding = 'utf-8'
            except UnicodeDecodeError:
                try:
                    f = open(self.fileName, mode = 'r', encoding = 'gbk')
                    data = f.readlines()
                    self.encoding = 'gbk'
                except:
                    print('FileNotFoundError')
                    r = False
            finally:
                f.close()
        print(self.encoding)
        if not r:
            return r
        else:
            return data
        
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          