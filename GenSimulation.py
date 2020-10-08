#!/usr/bin/python3
#@File: GenSimulation.py
#-*-coding:utf-8-*-
#@Author:cuijia
#python GenSimulation.py chr2.fasta svpos.txt svinfo.txt
import sys,random,numpy as np
interval = 2000
cnvlen = 1000
svlen = 200
number = 200
cnvnum = 100
cnvpro = [0.6,0.25,0.15]
delnum = 50
insnum = 40
invnum = 10

def LoadRef(file):
	ref = []
	with open(file,'r') as fin:
		fin.readline()
		while True:
			ch = fin.read(1)
			if not ch: break
			if ch!='\n' and ch!='\r':
				ref.append(ch)
		fin.close()
	return ref
def GenPos(length):
	pos = []
	flag = 0
	while(len(pos)<number):
		x = random.randint(interval,length-interval)
		if len(pos) == 0:
			pos.append(x)
		else:
			if x not in pos:
				for item in pos:
					if abs(x-item) > interval:
						flag = 1
					else:
						flag = 0
						break
				if flag == 1:
					pos.append(x)
			else:continue
	return pos
def GenString(length):
	base = ['A','T','C','G']
	base_seq = []
	for _ in range(length):
		base_seq.append(base[random.randint(0,3)])
	return base_seq
def GenCnv(ref,pos,fout,svinfo,count):
	cnv_num = cnvnum*cnvpro[0]
	cnvdel_num = cnvnum*cnvpro[1]
	cnvins_num = cnvnum*cnvpro[2]
	while count<cnv_num:
		copynum = random.randint(2,5)
		sequence = ref[pos[count]-1:pos[count]-1+cnvlen]*copynum
		fout.write(str(count+1)+'\t'+str(pos[count]+cnvlen)+'\t'+str(cnvlen*copynum)+'\t'
		           +str(random.randint(1,3))+"\t1\t0\t"+"".join(sequence)+'\n')
		svinfo.append([pos[count],count+1,cnvlen,copynum,0,0])
		count += 1
	while count<cnv_num+cnvdel_num:
		copynum = random.randint(2, 5)
		sequence = ref[pos[count] - 1:pos[count] - 1 + cnvlen] * copynum
		length = random.randint(cnvlen-svlen,cnvlen+svlen)
		while True:
			start = random.randint(0,len(sequence))
			if start + length <= len(sequence):
				break
		delseq = sequence[0:start]+sequence[start+length:]
		fout.write(str(count+1) + '\t' + str(pos[count] + cnvlen) + '\t' + str(cnvlen * copynum - length) + '\t'
		           + str(random.randint(1,3)) + "\t1\t0\t" + "".join(delseq)+'\n')
		svinfo.append([pos[count],count + 1,cnvlen,copynum,start,-length])
		count += 1
	while count<cnv_num+cnvdel_num+cnvins_num:
		copynum = random.randint(2, 5)
		sequence = ref[pos[count] - 1:pos[count] - 1 + cnvlen] * copynum
		length = random.randint(cnvlen - svlen, cnvlen + svlen)
		insertion = GenString(length)
		start = random.randint(0,len(sequence))
		insseq = sequence[0:start]+insertion+sequence[start:]
		fout.write(str(count+1) + '\t' + str(pos[count] + cnvlen) + '\t' + str(cnvlen * copynum + length) + '\t'
		           + str(random.randint(1,3)) + "\t1\t0\t" + "".join(insseq)+'\n')
		svinfo.append([pos[count], count + 1, cnvlen, copynum, start, length])
		count += 1
def GenDel(ref,pos,fout,svinfo,count):
	while count<cnvnum+delnum:
		length = random.randint(cnvlen - svlen, cnvlen + svlen)
		sequence = ref[pos[count]-1:pos[count]-1+length]
		fout.write(str(count+1)+'\t'+str(pos[count])+'\t'+str(-length)+'\t'
		           +str(random.randint(1,3))+"\t1\t0\t"+"".join(sequence)+'\n')
		svinfo.append([pos[count],count + 1,-length,0,0,0])
		count += 1
def GenIns(pos,fout,svinfo,count):
	while count<cnvnum+delnum+insnum:
		length = random.randint(cnvlen - svlen, cnvlen + svlen)
		sequence = GenString(length)
		fout.write(str(count+1)+'\t'+str(pos[count])+'\t'+str(length)+'\t'
		           +str(random.randint(1,3))+"\t1\t0\t"+"".join(sequence)+'\n')
		svinfo.append([pos[count], count + 1, length,0,0,0])
		count += 1
def GenInv(ref,pos,fout,svinfo,count):
	while count<cnvnum+delnum+insnum+invnum:
		length = random.randint(cnvlen - svlen, cnvlen + svlen)
		sequence = ref[pos[count] - 1:pos[count] - 1 + length]
		chrom = random.randint(1,3)
		fout.write(str(count+1)+'\t'+str(pos[count])+'\t'+str(-length)+'\t'
		           +str(chrom)+"\t1\t0\t"+"".join(sequence)+'\n')
		result = sequence[::-1]
		fout.write(str(count + 1) + '\t' + str(pos[count]) + '\t' + str(length) + '\t'
		           + str(chrom) + "\t1\t0\t" + "".join(result)+'\n')
		svinfo.append([pos[count],count + 1,length,0,pos[count],-length])
		count += 1
if __name__ == '__main__':
	#inputfile = 'chr2.fasta'
	#outputfile = 'svpos.txt'
	#outputcnv = 'svinfo.txt'
	inputfile = sys.argv[1]
	outputfile = sys.argv[2]
	outputcnv = sys.argv[3]
	fout = open(outputfile,'w')
	fout_sv = open(outputcnv, 'w')
	sv_info = []
	ref = LoadRef(inputfile)
	position = GenPos(len(ref))
	GenCnv(ref, position, fout, sv_info, 0)
	GenDel(ref, position, fout, sv_info, cnvnum)
	GenIns(position, fout, sv_info, cnvnum + delnum)
	GenInv(ref, position, fout, sv_info, cnvnum + delnum + insnum)
	sv_info = np.array(sv_info,dtype=int)
	sv_ins = sv_info[np.lexsort(sv_info[:, ::-1].T)]
	for line in sv_ins:
		for item in line:
			fout_sv.write(str(item)+'\t')
		fout_sv.write('\n')
	fout.close()
	fout_sv.close()

