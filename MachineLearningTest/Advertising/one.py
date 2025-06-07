import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#matplotlib inline

#显示中文
plt.rcParams['font.sans-serif'] = ['Arial']

#2.读取数据
#读取数据
dpath = "./data/"
df = pd.read_csv(dpath + "Advertising.csv")

#df.columns = ['记录号','电视广告费用', '广播广告费用', '报纸广告费用', '产品销量']
df.columns = ['ID','TV', 'radio', 'newspaper', 'sales']
#通过观察前5行，了解数据每列（特征）的概况
df.head()

#3.数据探索分析
# 数据总体信息
df.info()
# 对数值型特征，得到每个特征的描述统计量，查看特征的大致分布
df.describe()
#散点图查看单个特征与目标之间的关系
plt.scatter(df['TV'], df['sales'])
plt.xlabel('TV')
plt.ylabel('sales')

plt.scatter(df['radio'], df['sales'])
plt.xlabel('radio')
plt.ylabel('sales')

plt.scatter(df['newspaper'], df['sales'])
plt.xlabel('newspaper')
plt.ylabel('sales')

plt.xlim(0,300)
plt.ylim(0,300)

plt.scatter(df['TV'], df['radio'])
plt.xlabel('TV')
plt.ylabel('radio')

# 得到相关系数的绝对值，通常认为相关系数的绝对值大于0.6的特征为强相关
data_corr = df.corr()
data_corr = data_corr.abs()
sns.heatmap(data_corr,annot=True)
plt.show()

y = df['sales']
X = df.drop(['sales'], axis=1)

feat_names = X.columns
n_feats =X.columns.size

for i in range(n_feats):
    fig = plt.figure()
    plt.scatter(df[feat_names[i]], y)
    plt.xlabel(feat_names[i], fontsize=16)
    plt.ylabel('sales', fontsize=16)
    plt.show()