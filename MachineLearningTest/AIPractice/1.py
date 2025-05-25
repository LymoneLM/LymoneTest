# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# === 1. 加载数据 ===
data_path = "./data"
data = loadmat(data_path+'/spectra_data.mat')  # 替换为实际文件路径
NIR = data['NIR']  # 光谱数据 (60, 401)
octane = data['octane'].flatten()  # 辛烷值 (60,)

# === 2. 数据预处理 ===
# 标准化
scaler = StandardScaler()
Xn = scaler.fit_transform(NIR)

# 划分训练集测试集 (70%-30%)
X_train, X_test, y_train, y_test = train_test_split(Xn, octane, test_size=0.3, random_state=42)

# === 3. 构建BP神经网络 ===
model = Sequential([
    Dense(20, activation='tanh', input_shape=(401,)),  # 隐藏层20个神经元
    Dense(1)  # 输出层
])

# === 4. 训练配置 ===
model.compile(optimizer='adam', loss='mse')  # 使用Adam优化器

# === 5. 训练模型 ===
history = model.fit(
    X_train, y_train,
    epochs=500,
    batch_size=32,
    verbose=0  # 静默训练
)

# === 6. 预测 ===
y_train_pred = model.predict(X_train).flatten()
y_test_pred = model.predict(X_test).flatten()

# === 7. 性能评估 ===
# 计算相对误差 (MATLAB风格)
RE_train = np.mean(np.abs(y_train - y_train_pred)/y_train)
RE_test = np.mean(np.abs(y_test - y_test_pred)/y_test)

# 计算R²
SSres = np.sum((y_test - y_test_pred)**2)
SStot = np.sum((y_test - np.mean(y_test))**2)
R2 = 1 - SSres/SStot

print(f"测试集相对误差: {RE_test:.4f}")
print(f"决定系数 R²: {R2:.4f}")

# === 8. 结果可视化 ===
plt.figure(figsize=(10, 6))
plt.plot(y_test, 'bo-', label='真实值')
plt.plot(y_test_pred, 'r*--', label='预测值')
plt.xlabel('样本编号')
plt.ylabel('辛烷值')
plt.title('BP神经网络预测结果')
plt.legend()
plt.grid(True)
plt.show()