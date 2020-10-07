#!/usr/bin/python3
#@File: ExtractFPsv.py
#-*-coding:utf-8-*-

import os,pandas as pd

def LoadFileName(root):
	filename = []
	for file in os.listdir(root):
		if file.split('.')[0] == 'sv_unfiltered_info' and file.split('.')[1].isdigit():
			filename.append(file)
	return filename

if __name__ == '__main__':
	root = r"C:\Users\Administrator\Desktop\untitled\python3\real_data\data"
	Filelist = LoadFileName(root)
	for file in Filelist:
		outputfile_falsesv = "sv_false."+file.split('.')[1]+".csv"
		outputfile_truesv = "sv_true."+file.split('.')[1]+".csv"
		Numresult = "Numresult"+file.split('.')[1]+".txt"
		fout = open(Numresult,'w')
		sv_info = pd.read_csv(file, encoding='gbk', sep='\t')
		sv_info.loc[sv_info['FILTER'] == 'PASS', 'FILTER'] = 'F1'
		sv_info.loc[sv_info['FILTER'] != 'F1','FILTER'] = 'F2'
		sv_info.rename(columns={'FILTER': 'label'}, inplace=True)
		sv_info_label = sv_info.label
		sv_info = sv_info.drop('label', axis=1)
		sv_info.insert(len(sv_info.columns), 'label', sv_info_label)
		false_sv = sv_info[sv_info['label'] == 'F2']
		true_sv = sv_info[sv_info['label'] == 'F1']
		# sv_info.to_csv('test.csv',index=0,sep='\t')
		false_sv.to_csv(outputfile_falsesv, index=0, header=None,sep='\t')
		true_sv.to_csv(outputfile_truesv, index=0, header=None,sep='\t')
		fout.write("The number of false SV: %d\n" % false_sv.shape[0])
		fout.write("The number of true SV: %d\n" % true_sv.shape[0])
	fout.close()




