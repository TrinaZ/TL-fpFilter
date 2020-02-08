#!/usr/bin/python3
# @File: ClassifierOriginal.py
# -*-coding:utf-8-*-
# @Author:cuijia

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd, numpy as np

min_pur = 5
max_pur = 30
step = 5
train_time = 10

if __name__ == '__main__':
	outputfile = 'Accuracy.txt'
	fout = open(outputfile,'w')
	fout.write('Classifier: ExtraTreesClassifier \n')
	fout.write('Classify ten times to get the best accuracy, and then vote to get the final accuracy \n')
	file_list = []
	pur_list = []
	for i in range(min_pur, max_pur+step, step):
		pur_list.append(i)
		file_list.append("sv_feature." + str(i) + ".csv")
	data = []
	for file in file_list:
		data.append(pd.read_csv(file,encoding='gbk',sep='\t'))
	column = data[0].columns.tolist()
	col_name = column[:column.index('label')]
	for k in range(len(pur_list)):
		purity = pur_list[k]
		fout.write('purity: '+str(purity)+'\n')
		tar_file = file_list[k]
		test = data[k]
		feature_test = test[col_name]
		target_test = test['label']

		predict_array = []
		for j in range(len(file_list)):
			if file_list[k] != file_list[j]:
				src_file = file_list[j]
				train = data[j]
				feature_train = train[col_name]
				target_train = train['label']

				max_acc = 0
				for i in range(train_time):
					# clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(50,2), random_state=1)
					# clf = RandomForestClassifier(n_estimators=100,criterion='entropy',max_features='auto')
					clf = ExtraTreesClassifier(n_estimators=100, random_state=7, max_features='auto')
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
