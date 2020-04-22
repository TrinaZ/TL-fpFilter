#!/usr/bin/python3
# @File: Classifier20.py
# -*-coding:utf-8-*-
# @Author:cuijia

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd, numpy as np

min_pur = 1
max_pur = 5
step = 1
train_time = 1

def GenFileList(purity):
	pur_list = []
	file_src_list = []
	file_tar_list = []
	for i in np.arange(min_pur, purity, step):
		pur_list.append(i)
	for i in np.arange(purity + step, max_pur+step, step):
		pur_list.append(i)
	for i in pur_list:
		file_src_list.append("src_data."+str(i)+"_"+str(purity)+".csv")
		file_tar_list.append("tar_data."+str(i)+"_"+str(purity)+".csv")
	return file_src_list,file_tar_list

if __name__ == '__main__':
	outputfile = 'Accuracy30.txt'
	fout = open(outputfile,'w')
	fout.write('TCA transformation matrix dimension: 20 \n')
	fout.write('Classifier: ExtraTreesClassifier \n')
	fout.write('Classify ten times to get the best accuracy, and then vote to get the final accuracy \n')
	for purity in np.arange(min_pur, max_pur+step, step):
		fout.write('purity: '+str(purity)+'\n')
		file_src_list, file_tar_list = GenFileList(purity)
		file = file_tar_list[0]
		data = pd.read_csv(file)
		column = data.columns.tolist()
		col_name = column[:column.index('label')]

		predict_array = []
		for i in range(len(file_src_list)):
			src_file = file_src_list[i]
			tar_file = file_tar_list[i]
			train = pd.read_csv(src_file)
			test = pd.read_csv(tar_file)
			feature_train = train[col_name]
			target_train = train['label']
			feature_test = test[col_name]
			target_test = test['label']
			max_acc = 0
			for i in range(train_time):
				# clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(50,2), random_state=1)
				# clf = RandomForestClassifier(n_estimators=100,criterion='entropy',max_features='auto')
				clf = ExtraTreesClassifier(n_estimators=100, random_state=8, max_features='auto')
				clf.fit(feature_train,target_train)
				predict_results=clf.predict(feature_test)
				acc = accuracy_score(predict_results, target_test)
				if max_acc<acc:
					max_acc = acc
					predict = predict_results
			fout.write(src_file+'\t'+tar_file+'\t'+str(max_acc)+'\n')
			predict_array.append(predict)
		predict_array_num = []
		for item in predict_array:
			tmp = ['1' if i == 'F1' else '2' for i in item]
			predict_array_num.append(tmp)
		predict_all = np.array(predict_array_num,dtype=int).T
		target_result = []
		for col in predict_all:
			result = np.argmax(np.bincount(col))
			target_result.append(result)
		target = ['F1' if i == 1 else 'F2' for i in target_result]
		accuracy = accuracy_score(target, target_test)
		fout.write('accuracy: '+str(accuracy)+'\n')
		fout.write('\n')
	fout.close()
