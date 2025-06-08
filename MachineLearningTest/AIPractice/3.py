# SVM分类
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体支持
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 导入数据
df = pd.read_excel('./data/student.xlsx', sheet_name='Sheet1')

X = df[['Height', 'Weight']].values
y = df['Label'].values

# 划分训练集和测试集
np.random.seed(0)  # 固定随机种子
indices = np.random.permutation(len(df))
X_train = X[indices[:200]]
y_train = y[indices[:200]]
X_test = X[indices[200:260]]
y_test = y[indices[200:260]]

# 归一化
scaler = MinMaxScaler(feature_range=(0, 1))
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 标准化
standardizer = StandardScaler()
X_train_std = standardizer.fit_transform(X_train_scaled)
X_test_std = standardizer.transform(X_test_scaled)

# 训练模型
model = svm.SVC(
    kernel='rbf',
    C=9,
    gamma='scale'
)
model.fit(X_train_std, y_train)

# SVM预测
train_pred = model.predict(X_train_std)
test_pred = model.predict(X_test_std)

# 计算准确率
train_accuracy = np.mean(train_pred == y_train) * 100
test_accuracy = np.mean(test_pred == y_test) * 100

print(f"训练集准确率: {train_accuracy:.2f}%")
print(f"测试集准确率: {test_accuracy:.2f}%")

# 组合结果
train_results = np.vstack((y_train, train_pred)).T
test_results = np.vstack((y_test, test_pred)).T

# 绘图
plt.figure(figsize=(12, 6))
x_range = np.arange(1, len(y_test) + 1)

plt.plot(x_range, y_test, 'r-*', linewidth=1.5, label='真实类别')
plt.plot(x_range, test_pred, 'b:o', linewidth=1.5, label='预测类别')

plt.grid(True)
plt.legend(loc='best')
plt.xlabel('测试集样本编号')
plt.ylabel('测试集样本类别')
plt.title(f'测试集SVM预测结果对比(RBF核函数)\n准确率 = {test_accuracy:.2f}%')
plt.tight_layout()
plt.show()