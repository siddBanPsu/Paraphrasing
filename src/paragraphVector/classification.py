'''
Created on Mar 10, 2015

@author: sub253
'''
import csv
import numpy as np
import random
from nolearn.dbn import DBN
from sklearn import metrics
from sklearn.metrics import classification_report
import codecs
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import scale
from numpy import dtype
from sklearn.svm.libsvm import cross_validation
from UnbalancedDataset import *
from sklearn.svm.classes import SVC
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble.forest import RandomForestClassifier



file_to_read='../inputFile/Diseases_and_disorders.corpus.pos.txt.s2v.vec'
with open(file_to_read) as f:
    lines = f.readlines()[1:]

#print lines[0]

ncols=len(lines[0].split(' '))       

print ncols
data = np.loadtxt(file_to_read, delimiter=' ', skiprows=1, usecols=range(1,ncols))
print len(data[0])

print len(data)
category='Diseases_and_disorders'


class_list=[]
with open('../inputFile/'+category+'.corpus.txt') as f:
    reader=csv.reader(f,delimiter='\t')
    for class_name,x,content in reader:
        class_list.append(class_name)

print len(class_list)

numInstance=len(class_list)

list_random=random.sample(range(0, len(class_list)), numInstance)
f_data=np.zeros((numInstance,ncols-1))


class_temp=[]
i=0
for rNum in list_random:
    f_data[i]=data[rNum]
    #print class_list[rNum]
    class_temp.append(class_list[rNum])
    i=i+1

print len(f_data)     
     

#print f_data[6],f_class[6]
f_class = np.zeros((numInstance))
myset = set(class_temp)

print(myset)
# CREATE integer labels
classmap ={}
i=0
for x in myset:
    classmap[x]=i
    i=i+1
 
for k in range(numInstance):
    f_class[k]=classmap[class_temp[k]] 

print(f_class)

X_folds = np.array_split(f_data, 10)
#print(X_folds)
y_folds = np.array_split(f_class, 10)


# clf = DBN(
#     [-1, 300, -1],
#         learn_rates = 0.2,
#     learn_rate_decays = 0.9,
#     learn_rates_pretrain=0.005,
#     #learn_rates=0.3,
#     epochs=50,
#     scales=0.02
#     )

clf=SVC(class_weight='auto')

f_class=f_class.astype(float)

scores = cross_val_score(clf, f_data, f_class, cv=10, scoring='f1')

#print metrics.precision_score(scores)
print "P:",scores
print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)     
     
     
     
     
scores = list()
# f = codecs.open('results.classification.txt.2','w',"utf-8")
# for k in range(10):
#     print("Running fold "+str(k))
#     # We use 'list' to copy, in order to 'pop' later on
#     X_train = list(X_folds)
#     X_test  = X_train.pop(k)
#     X_train = np.concatenate(X_train)
#     y_train = list(y_folds)
#     y_test  = y_train.pop(k)
#     y_train = np.concatenate(y_train)
#     
#     dbn = DBN(
#     [X_train.shape[1], 300, 10],
#     learn_rates = 0.2,
#     learn_rate_decays = 0.9,
#     learn_rates_pretrain=0.005,
#     epochs = 50,
#     verbose = 0)
#     dbn.fit(X_train, y_train)
# 
#     preds = dbn.predict(X_test)
#     
#     print 'The precision for this classifier is ' + str(metrics.precision_score(y_test, preds))
#     print 'The recall for this classifier is ' + str(metrics.recall_score(y_test, preds))
#     print 'The f1 for this classifier is ' + str(metrics.f1_score(y_test, preds))
#     print 'The accuracy for this classifier is ' + str(metrics.accuracy_score(y_test, preds))
#     f.write('Fold '+str(k)+'||'+str(metrics.precision_score(y_test, preds))+'||'+str(metrics.recall_score(y_test, preds))+'||'+str(metrics.f1_score(y_test, preds))+'\n')
#     print('\nHere is the confusion matrix:')
#     print(metrics.confusion_matrix(y_test, preds, labels=np.unique(f_class)))
#     cf=str(metrics.confusion_matrix(y_test, preds, labels=np.unique(f_class)));
#     cf=cf.decode('utf-8')
#     f.write(cf)
#   
#     print classification_report(y_test, preds)
#     f.write(classification_report(y_test, preds).decode('utf-8'))
# #print(scores)
# 
# f.close()



# with open('../inputFile/'+category+'.corpus.txt') as f:
#     reader=csv.reader(f,delimiter='\t')
#     for class_name,x,content in reader:
#         if class_name.lower() in ['treatment']:
#             print content
        

     