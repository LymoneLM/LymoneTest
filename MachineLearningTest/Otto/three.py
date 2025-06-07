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
df = pd.read_csv(dpath + "Advertising.csv")

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
print("\n最小二乘回归结果:")
print(f"测试集 R2: {r2_score(y_test, y_test_pred_lr):.4f}")
print(f"训练集 R2: {r2_score(y_train, y_train_pred_lr):.4f}")

#################岭回归，要求调参
from sklearn.linear_model import  RidgeCV
from sklearn.linear_model import LassoCV
########弹性网，要求调参
from sklearn.linear_model import ElasticNetCV
# ====================== 岭回归 (10个不同alpha) ======================
alphas_ridge = np.logspace(-2, 2, 10)  # 10个对数均匀分布的正则化参数
ridge_results = []
for alpha in alphas_ridge:
    ridge = RidgeCV(alphas=alpha)
    ridge.fit(X_train, y_train)
    test_r2 = r2_score(y_test, ridge.predict(X_test))
    train_r2 = r2_score(y_train, ridge.predict(X_train))
    ridge_results.append((alpha, train_r2, test_r2))

print("\n岭回归结果 (10个不同正则化参数):")
print("Alpha\t\t训练集R2\t\t测试集R2")
for alpha, train_r2, test_r2 in ridge_results:
    print(f"{alpha:.6f}\t{train_r2:.4f}\t\t{test_r2:.4f}")
# ====================== Lasso回归 ======================
lasso = LassoCV(alphas=np.logspace(-4, 0, 100), cv=5)
lasso.fit(X_train, y_train)
y_test_pred_lasso = lasso.predict(X_test)
y_train_pred_lasso = lasso.predict(X_train)

print("\nLasso回归结果:")
print(f"最佳alpha: {lasso.alpha_:.6f}")
print(f"测试集 R2: {r2_score(y_test, y_test_pred_lasso):.4f}")
print(f"训练集 R2: {r2_score(y_train, y_train_pred_lasso):.4f}")

# ====================== 弹性网 (10个不同L1比率) ======================
l1_ratios = np.linspace(0.01, 0.99, 10)  # 10个不同的L1比率
elastic_results = []

for l1_ratio in l1_ratios:
    elastic_net = ElasticNetCV(l1_ratio=[l1_ratio], alphas=np.logspace(-4, 0, 50), cv=5)
    elastic_net.fit(X_train, y_train)
    test_r2 = r2_score(y_test, elastic_net.predict(X_test))
    train_r2 = r2_score(y_train, elastic_net.predict(X_train))
    elastic_results.append((l1_ratio, train_r2, test_r2))

print("\n弹性网结果 (10个不同L1比率):")
print("L1_Ratio\t训练集R2\t\t测试集R2")
for l1_ratio, train_r2, test_r2 in elastic_results:
    print(f"{l1_ratio:.2f}\t\t{train_r2:.4f}\t\t{test_r2:.4f}")


# # 创建包含四个列表数据的字典
# data = {
#     'ridge_r2_scores_test': ridge_r2_scores_test,
#     'ridge_r2_scores_train': ridge_r2_scores_train,
#     'elastic_net_r2_scores_test': elastic_net_r2_scores_test,
#     'elastic_net_r2_scores_train': elastic_net_r2_scores_train,
#     'lasso_r2_scores_test': lasso_r2_scores_test,
#     'lasso_r2_scores_train': lasso_r2_scores_train
# }
#
# # 将字典转换为 DataFrame
# df = pd.DataFrame(data)
#
# # 将 DataFrame 导出为 Excel 文件
# df.to_excel('r2_scores0.7.xlsx', index=False)

