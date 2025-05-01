import numpy as np
import pandas as pd
import numpy as np
import pandas as pd


#1. 定义数据归一化方法
def feature_normalize(dataset):#zscore标准化
    mu = np.mean(dataset, axis=0)#对各列求均值，返回 1* n 矩阵
    sigma = np.std(dataset, axis=0)
    return (dataset - mu) / sigma

#2.加载数据, 进行标准化
data = pd.read_csv('TaiwanRawDataSample.csv')
data.head()
dataX= data.iloc[:,:-1]
data_label = data.iloc[:, -1]

#用zscore标准化
Standard_data = feature_normalize(dataX.iloc[:,:].values)

#3.输出结果到本地(将23行路径替换为自己本地的地址)
Standard_data=pd.DataFrame(Standard_data)
Standard_data= Standard_data.join(data_label)

writer = pd.ExcelWriter('Standard_TaiwanRawDataSample.xlsx')

Standard_data.to_excel(writer, index=False, header=False)
# writer.save()
writer.close()





