#!/usr/bin/python3
#@File: ExtractSvInfo.py
#-*-coding:utf-8-*-
#@Author:cuijia
#python3 ExtractSvInfo.py speed.sv.vcf speed.sv_info.csv
import sys,csv
from operator import itemgetter

def extractInLine1(string,label):
	dic = dict()
	if string.find('IMPRECISE') != -1:
		dic['IMPRECISE'] = '1'
	else:
		dic['IMPRECISE'] = '0'
	string = string.split(';')
	for item in string:
		item = item.split('=')
		if len(item)==2:
			dic[item[0]] = item[1]
	res = itemgetter(*label)(dic)
	result = dict(zip(label, res))
	return result
def extractInLine2(label,string):
	label = label.split(':')
	string = string.split(':')
	dic = dict(zip(label, string))
	return dic
if __name__ == '__main__':
	info_name = ['CHROM','POS','SVTYPE','SVLEN','END','IMPRECISE','CIPOS','CIEND','CIPOS95','CIEND95',
	             'GT','SU','PE','SR','GQ','SQ','GL','DP','RO','AO','QR','QA','RS','AS','ASC','RP','AP','AB','CN']
	label = ['SVTYPE','SVLEN','END','IMPRECISE','CIPOS','CIEND','CIPOS95','CIEND95']
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	#input_file = "speed.sv.vcf"
	#output_file = "speed.sv_info.csv"
	fin = open(input_file,'r')
	fout = open(output_file,'w',newline='')
	info_list = []
	for line in fin.readlines():
		if line[0] == '#':
			continue
		else :
			info = dict()
			line = line.split()
			info['CHROM'] = line[0]
			info['POS'] = line[1]
			temp = line[7]
			result1 = extractInLine1(temp,label)
			result2 = extractInLine2(line[8],line[9])
			z = result1.copy()
			z.update(result2)
			dicts = info.copy()
			dicts.update(z)
			info_list.append(dicts)
	headers = info_name
	writer = csv.DictWriter(fout, fieldnames=headers,delimiter='\t')
	writer.writeheader()
	for row in info_list:
		writer.writerow(row)
	fin.close()
	fout.close()
