#!/usr/bin/python3
#@File: GenFeature.py
#-*-coding:utf-8-*-
#@Author:cuijia
#python GenFeature.py sv_true.csv sv_false.csv sv_feature.csv

import sys,numpy as np,pandas as pd

def genFeature(feature):
	feature_label = ['CHROM','POS','SVTYPE','SVLEN','END','IMPRECISE','CIPOS','CIEND','CIPOS95','CIEND95','GT','SU','PE','SR','GQ',
					'SQ','GL','DP','RO','AO','QR','QA','RS','AS','ASC','RP','AP','AB','CN']
	feature_label1 = ['IMPRECISE','CIPOS','CIEND','CIPOS95','CIEND95','GT','SU','PE','SR','GQ',
					'SQ','GL1','GL2','GL3','DP','RO','AO','QR','QA','RS','AS','ASC','RP','AP','AB','CN']
	feature.columns = feature_label
	feature_gt = feature['GT'].str.split('/', expand=True).astype(int)
	feature['GT'] = feature_gt[0] + feature_gt[1]
	list = ['CIPOS','CIEND','CIPOS95','CIEND95']
	for item in list:
		feature_temp = feature[item].str.split(',', expand=True).astype(int)
		feature[item] = feature_temp[1] - feature_temp[0]
	feature_gl = feature['GL'].str.split(',', expand=True).astype(int)
	GL = ['GL1', 'GL2', 'GL3']
	feature_gl.columns = GL
	col_name = feature.columns.tolist()
	col_name = col_name[:col_name.index('GL')] + GL + col_name[col_name.index('GL'):]
	feature = feature.reindex(columns=col_name)
	feature[GL] = feature_gl.values
	feature.drop('GL', axis=1, inplace=True)
	feature = feature[feature_label1]
	return feature
if __name__ == '__main__':
	inputfile1 = sys.argv[1]
	inputfile2 = sys.argv[2]
	outputfile = sys.argv[3]
	sv_true = pd.read_csv(inputfile1, encoding='gbk', header=None, sep='\t')
	sv_false = pd.read_csv(inputfile2, encoding='gbk', header=None, sep='\t')
	feature1 = genFeature(sv_true)
	feature2 = genFeature(sv_false)
	feature1['label'] = 'F1'
	feature2['label'] = 'F2'
	feature = pd.concat([feature1,feature2], ignore_index=True)
	feature.to_csv(outputfile, index=0,sep=str('\t'))
	
	

	
