#!/usr/bin/python3
#@File: FalsePositiveSV.py
#-*-coding:utf-8-*-
#@Author:cuijia
#python ExtractFPsv.py svinfo.txt sv_info.csv Accresult.txt sv_false.csv sv_true.csv
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#from sklearn.model_selection import train_test_split
import sys,numpy as np,pandas as pd

def loadSvPos(file):
	svInfo = []
	with open(file,'r') as fin:
		for line in fin.readlines():
			line = line.split()
			temp = [line[0],line[2]]
			svInfo.append(temp)
	return svInfo
def writeInfo(sv_ins,sv_ins_csv,outputfile_sv_inspos,outputfile_sv_pos):
	fout1 = open(outputfile_sv_inspos, 'w')
	for i in range(sv_ins.shape[0]):
		for item in sv_ins[i]:
			fout1.write(str(item)+'\t')
		fout1.write('\n')
	sv_ins_csv.to_csv(outputfile_sv_pos, index=0, sep='\t')
def markLabel(sv_ins,sv_ins_csv_val):
	sv_label_csv = [0]*sv_ins_csv_val.shape[0]
	sv_label_ins = [0]*sv_ins.shape[0]
	mark_info = []
	threshold = 0
	for i in range(sv_ins.shape[0]):
		for j in range(sv_ins_csv_val.shape[0]):
			begin = sv_ins[i][0]
			end = sv_ins[i][0] + abs(sv_ins[i][1])
			CIPOS = sv_ins_csv_val[j][5].split(',')
			begin1 = sv_ins_csv_val[j][0] + int(CIPOS[0]) - threshold
			begin2 = sv_ins_csv_val[j][0] + int(CIPOS[1]) + threshold
			CIEND = sv_ins_csv_val[j][6].split(',')
			end1 = sv_ins_csv_val[j][3] + int(CIEND[0]) - threshold
			end2 = sv_ins_csv_val[j][3] + int(CIEND[1]) + threshold
			if sv_ins_csv_val[j][0] > end:
				break
			if begin1 <= begin <= begin2 and end1 <= end <= end2:
				sv_label_ins[i] = 1
				sv_label_csv[j] = 1
				mark_info.append([begin,sv_ins[i][1],sv_ins_csv_val[j][0],
				                  sv_ins_csv_val[j][5],sv_ins_csv_val[j][6],sv_ins_csv_val[j][2]])
	return sv_label_csv,sv_label_ins,mark_info
def countTPFPAcc(sv_label_ins,sv_label_csv,outfile):
	snp_Acc = round(sv_label_ins.count(1) / len(sv_label_ins) * 100, 4)
	snp_TP = round(sv_label_csv.count(1) / len(sv_label_csv) * 100, 4)
	snp_FP = round((1 - sv_label_csv.count(1) / len(sv_label_csv)) * 100, 4)
	with open(outfile,'w') as fout:
		fout.write("The actual number of SVs: " + str(len(sv_label_ins))+'\n')
		fout.write("The detected number of SVs: " + str(len(sv_label_csv))+'\n')
		fout.write("The actual number of detected SVs: " + str(sv_label_ins.count(1))+'\n')
		fout.write("SVs Accuracy: " + str(snp_Acc)+'\n')
		fout.write("SVs True Positive: " + str(snp_TP)+'\n')
		fout.write("SVs False Positive: " + str(snp_FP)+'\n')

if __name__ == '__main__':
	#inputfile_ins = "svinfo.txt"
	#inputfile_sv = "speed.sv_info.csv"
	inputfile_ins = sys.argv[1]
	inputfile_sv = sys.argv[2]
	sv_ins = np.array(loadSvPos(inputfile_ins),dtype=int)
	#sv_ins = sv_ins[np.lexsort(sv_ins[:,::-1].T)]
	sv_info = pd.read_csv(inputfile_sv, encoding='gbk', sep='\t')
	label = ['POS','SVTYPE', 'SVLEN', 'END', 'IMPRECISE', 'CIPOS', 'CIEND']
	sv_ins_csv = sv_info[label]
	sv_ins_csv_val = sv_ins_csv.values
	sv_label_csv, sv_label_ins,mark_info = markLabel(sv_ins, sv_ins_csv_val)
	#TP,FP
	#Accresult = "Accresult.txt"
	Accresult = sys.argv[3]
	countTPFPAcc(sv_label_ins, sv_label_csv, Accresult)
	#FPsv,TPsv feature
	mark_info = np.array(mark_info)
	true_sv = sv_info[sv_info['POS'].isin(mark_info[:,2].tolist())]
	false_sv = sv_info[~(sv_info['POS'].isin(mark_info[:,2].tolist()))]
	outputfile_falsesv = sys.argv[4]
	outputfile_truesv = sys.argv[5]
	#outputfile_falsesv = "sv_false.csv"
	#outputfile_truesv = "sv_true.csv"
	false_sv.to_csv(outputfile_falsesv, index=0, header=None,sep=str('\t'))
	true_sv.to_csv(outputfile_truesv, index=0, header=None,sep=str('\t'))
	# outputfile_mark = "markinfo.txt"
	# outputfile_mark = sys.argv[5]
	# fout_mark = open(outputfile_mark,'w')
	# for line in mark_info:
	# 	for item in line:
	# 		fout_mark.write(str(item)+'\t')
	# 	fout_mark.write('\n')



