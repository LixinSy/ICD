# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 19:44:00 2017

@author: 李莘
"""

import pandas as pd
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext


conf = SparkConf().setMaster('local').setAppName('test')
sc = SparkContext(conf = conf)
sqlContext = SQLContext(sc)

#filePath = r'./data/t2dmtest.csv'
#df = pd.read_csv(filePath, encoding = 'utf-8', skip_blank_lines = False)
col = ['名字', '学号', '年龄']
name = ['李莘', '李莘', '唐皓月']
num = ['053025', '053025', '053061']
age = [20, 20, 21]

data = {'名字':name, '学号':num, '年龄':age}
df = pd.DataFrame(data)

spk_df = sqlContext.createDataFrame(df)























