#!/usr/bin/python3
#@File: ChangeName23.py
#-*-coding:utf-8-*-
#@Author:cuijia

import pandas as pd
import os
#os.listdir(os.getcwd())

#os.chdir(os.getcwd())
#def Loadfilename(root):
root = r"C:\data1\1"
file = os.listdir(root)
file_list = []

src_data = "src_data.1_1.csv"
data = pd.read_csv(src_data)
column = data.columns

for i in range(len(file)):
	if file[i].split('.')[0]=='tar_data' and file[i].endswith('csv'):
		file_list.append(file[i])

for item in file_list:
	df = pd.read_csv(item)
	df.columns = column
	df.to_csv(item, index=0)
