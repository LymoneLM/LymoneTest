import os
from scipy.io import loadmat

data_path = "./data"
data = loadmat(data_path+"/spectra_data.mat")
octane = data["octane"]
NIR = data["NIR"]


import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2

# 假设NIR和octane已加载为numpy数组，示例数据需替换为实际数据
X = np.array(NIR)  # 形状(60, 401)
y = np.array(octane)  # 形状(60,)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化输入数据
scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)

# 构建BP神经网络模型
model = Sequential([
    Dense(64, activation='relu', kernel_regularizer=l2(0.01), input_shape=(401,)),
    Dropout(0.3),
    Dense(32, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.3),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# 早停法，监控验证集损失
early_stop = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

# 训练模型
history = model.fit(
    X_train_scaled, y_train,
    epochs=1000,
    batch_size=8,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=0
)

# 预测测试集
y_pred = model.predict(X_test_scaled).flatten()

# 计算评价指标
mape = mean_absolute_percentage_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"相对误差（MAPE）: {mape:.4f}")
print(f"决定系数R²: {r2:.4f}")