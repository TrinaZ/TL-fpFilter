#!/usr/bin/python3
#@File: GenFeature.py
#-*-coding:utf-8-*-
#@Author:cuijia

import os,pandas as pd,numpy as np

def LoadFileName(root):
	file_false = []
	file_true = []
	for file in os.listdir(root):
		if file.split('.')[0] == 'sv_false' and file.split('.')[1].isdigit():
			file_false.append(file)
		if file.split('.')[0] == 'sv_true' and file.split('.')[1].isdigit():
			file_true.append(file)
	return file_false,file_true

def genFeature(feature):
	feature_label = ['CHROM','POS','QUAL','DISC_MAPQ','EVDNC','IMPRECISE','MAPQ','MATENM','NM','NUMPARTS',
	                 'SECONDARY','GT','AD','DP','GQ','PL','SR','DR','LR','LO','label']
	feature_label1 = ['QUAL','DISC_MAPQ','EVDNC','IMPRECISE','MAPQ','MATENM','NM','NUMPARTS',
	                 'SECONDARY','GT','AD','DP','GQ','PL1','PL2','PL3','SR','DR','LR','LO','label']
	feature.columns = feature_label
	feature_gt = feature['GT'].str.split('/', expand=True).astype(int)
	feature['GT'] = feature_gt[0] + feature_gt[1]
	feature_pl = feature['PL'].str.split(',', expand=True).astype(float)
	PL = ['PL1', 'PL2', 'PL3']
	feature_pl.columns = PL
	col_name = feature.columns.tolist()
	col_name = col_name[:col_name.index('PL')] + PL + col_name[col_name.index('PL'):]
	feature = feature.reindex(columns=col_name)
	feature[PL] = feature_pl.values
	feature.drop('PL', axis=1, inplace=True)
	EVDNC_NUM = []
	for str in feature['EVDNC']:
		num = 0
		for i in str:
			num += ord(i)
		EVDNC_NUM.append(num)
	feature['EVDNC'] = EVDNC_NUM
	feature = feature[feature_label1]
	return feature
if __name__ == '__main__':
	root = r"/home/cuijia/Data/chr2_sv/feature50"
	file_false, file_true = LoadFileName(root)
	for i in range(len(file_false)):
		inputfile1 = file_true[i]
		inputfile2 = file_false[i]
		outputfile = 'sv_feature.'+file_false[i].split('.')[1]+".csv"
		sv_true = pd.read_csv(inputfile1, encoding='gbk', header=None, sep='\t')
		sv_false = pd.read_csv(inputfile2, encoding='gbk', header=None, sep='\t')
		feature1 = genFeature(sv_true)
		feature2 = genFeature(sv_false)
		feature = pd.concat([feature1,feature2], ignore_index=True)
		feature.to_csv(outputfile, index=0,sep=str('\t'))
	
	

	
