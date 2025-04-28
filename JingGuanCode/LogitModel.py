from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn import model_selection
from sklearn import metrics
from sklearn.metrics import roc_curve, auc, confusion_matrix,f1_score,accuracy_score,log_loss
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score


data = np.genfromtxt("Train_Standard_TaiwanRawDataSample.csv", delimiter=",")
x_train = data[:, :-1]
y_train = data[:, -1]

data_test = np.genfromtxt("Test_Standard_TaiwanRawDataSample.csv", delimiter=",")
x_test = data_test[:, :-1]
y_test = data_test[:, -1]


clf = LogisticRegression(penalty = 'l1', solver='liblinear')
#penalty='l1'，代表模型使用l1范数来约束自变量，和lasso回归中的惩罚函数一样，都有对自变量的控制作用
clf.fit(x_train,y_train)
pre_y = clf.predict(x_test)
print(metrics.classification_report(y_test,pre_y))
## plot ROC曲线
pre_y_p = clf.predict_proba(x_test)[:, 1]

fpr_LR, tpr_LR, _ = metrics.roc_curve(y_test, pre_y_p)
auc = metrics.auc(fpr_LR, tpr_LR)
plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr_LR, tpr_LR,"r",linewidth = 2)
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.title('Logistic ROC curve')
plt.text(0.2,0.8,"auc = "+str(round(auc,4)))
plt.show()
