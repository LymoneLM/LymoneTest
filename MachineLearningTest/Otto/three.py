#数据处理
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline
import seaborn as sns
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

#显示中文
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

#读取数据
dpath = "./data/"
df = pd.read_csv(dpath + "FE_Advertising.csv")

#通过观察前5行，了解数据每列（特征）的概况
df.head()
# 数据总体信息
df.info()

# 从原始数据中分离输入特征x和输出y
y = df['sales']
X = df.drop('sales', axis = 1)

#特征名称，用于后续显示权重系数对应的特征
feat_names = X.columns

# 随机采样20%的数据构建测试样本，其余作为训练样本
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.2)
#X_train.shape

###########最小二乘，要求调参
# 线性回归
from sklearn.linear_model import LinearRegression

# 1.使用默认配置初始化学习器实例
lr = LinearRegression()

# 2.用训练数据训练模型参数
lr.fit(X_train, y_train)

# 3. 用训练好的模型对测试集进行预测
y_test_pred_lr = lr.predict(X_test)
y_train_pred_lr = lr.predict(X_train)

#性能评估，R方分数
print("The r2 score of LinearRegression on test is %f" %(r2_score(y_test, y_test_pred_lr)))
print("The r2 score of LinearRegression on train is %f" %(r2_score(y_train, y_train_pred_lr)))

#################岭回归，要求调参
from sklearn.linear_model import  RidgeCV
from sklearn.linear_model import LassoCV
########弹性网，要求调参
from sklearn.linear_model import ElasticNetCV
alphas = np.arange(0.01, 10, 0.01) # 定义超参数范围
l1_ratios=np.arange(0.01, 1, 0.01)
ridge_r2_scores_test = [] # 用于存储 Ridge 模型在测试集上的 r2_score
ridge_r2_scores_train = [] # 用于存储 Ridge 模型在训练集上的 r2_score
lasso_r2_scores_test=[];
lasso_r2_scores_train=[];
elastic_net_r2_scores_test = [] # 用于存储 ElasticNet 模型在测试集上的 r2_score
elastic_net_r2_scores_train = [] # 用于存储 ElasticNet 模型在训练集上的 r2_score
for alpha in alphas:
    #1. 设置超参数（正则参数）范围
    #alphas = [ 0.02]
    print(alpha)
    #2. 生成一个RidgeCV实例
    ridge = RidgeCV(alphas=alpha, store_cv_values=True)

    #3. 模型训练
    ridge.fit(X_train, y_train)

    #4. 预测
    y_test_pred_ridge = ridge.predict(X_test)
    y_train_pred_ridge = ridge.predict(X_train)

    #模型性能评估
    #print("The r2 score of Ridge on test is %f" %(r2_score(y_test, y_test_pred_ridge)))
    #print("The r2 score of Ridge on train is %f" %(r2_score(y_train, y_train_pred_ridge)))
    ridge_r2_scores_test.append(r2_score(y_test, y_test_pred_ridge))
    ridge_r2_scores_train.append(r2_score(y_train, y_train_pred_ridge))

    # 1. 设置超参数搜索范围
    # Lasso可以自动确定最大的alpha，所以另一种设置alpha的方式是设置最小的alpha值（eps） 和 超参数的数目（n_alphas），
    # 然后LassoCV对最小值和最大值之间在log域上均匀取值n_alphas个
    # np.logspace(np.log10(alpha_max * eps), np.log10(alpha_max),num=n_alphas)[::-1]

    # 2 生成LassoCV实例（默认超参数搜索范围）
    lasso = LassoCV(alphas=[alpha])

    # 3. 训练（内含CV）
    lasso.fit(X_train, y_train)

    # 4. 测试
    y_test_pred_lasso = lasso.predict(X_test)
    y_train_pred_lasso = lasso.predict(X_train)

    # 评估，使用r2_score评价模型在测试集和训练集上的性能
    #print("The r2 score of lasso on test is %f" % (r2_score(y_test, y_test_pred_lasso)))
    #print("The r2 score of lasso on train is %f" % (r2_score(y_train, y_train_pred_lasso)))
    lasso_r2_scores_test.append(r2_score(y_test, y_test_pred_lasso))
    lasso_r2_scores_train.append(r2_score(y_train, y_train_pred_lasso))
    #for l1_ratio in l1_ratios:
    # 1. 设置超参数搜索范围
    # Lasso可以自动确定最大的alpha，所以另一种设置alpha的方式是设置最小的alpha值（eps） 和 超参数的数目（n_alphas），
    # 然后LassoCV对最小值和最大值之间在log域上均匀取值n_alphas个
    # np.logspace(np.log10(alpha_max * eps), np.log10(alpha_max),num=n_alphas)[::-1]
    #l1_ratio = [0.01]

    # 2 ElasticNetCV（设置超参数搜索范围）
    elastic_net = ElasticNetCV(l1_ratio=0.7,alphas=[alpha])

    # 3. 训练（内含CV）
    elastic_net.fit(X_train, y_train)

    # 4. 测试
    y_test_pred_elastic_net = elastic_net.predict(X_test)
    y_train_pred_elastic_net = elastic_net.predict(X_train)

    # 评估，使用r2_score评价模型在测试集和训练集上的性能
    #print("The r2 score of elastic_net on test is %f" % (r2_score(y_test, y_test_pred_elastic_net)))
    #print("The r2 score of elastic_net on train is %f" % (r2_score(y_train, y_train_pred_elastic_net)))
    elastic_net_r2_scores_test.append(r2_score(y_test, y_test_pred_elastic_net))
    elastic_net_r2_scores_train.append(r2_score(y_train, y_train_pred_elastic_net))

################lasso要求调参

import pandas as pd

# 创建包含四个列表数据的字典
data = {
    'ridge_r2_scores_test': ridge_r2_scores_test,
    'ridge_r2_scores_train': ridge_r2_scores_train,
    'elastic_net_r2_scores_test': elastic_net_r2_scores_test,
    'elastic_net_r2_scores_train': elastic_net_r2_scores_train,
    'lasso_r2_scores_test': lasso_r2_scores_test,
    'lasso_r2_scores_train': lasso_r2_scores_train
}

# 将字典转换为 DataFrame
df = pd.DataFrame(data)

# 将 DataFrame 导出为 Excel 文件
df.to_excel('r2_scores0.7.xlsx', index=False)

