import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# 读取数据
dataset = pd.read_excel('Standard_TaiwanRawDataSample.xlsx') # 8V1gedaitrain_lable  20V1gedaitrain


X, y = dataset.iloc[:,:-1], dataset.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, shuffle=True)

traindata= X_train.join(y_train)
testdata= X_test.join(y_test)


# 输出表
traindata.to_csv('Train_Standard_TaiwanRawDataSample.csv', index=False, header=False)
testdata.to_csv('Test_Standard_TaiwanRawDataSample.csv', index=False, header=False)
