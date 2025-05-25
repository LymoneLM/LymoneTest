from scipy.io import loadmat

data_path = "./data"
data = loadmat(data_path+"/spectra_data.mat")
octane = data["octane"]
NIR = data["NIR"]


# 1-导入包库
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score

# 2-加载数据
X = NIR
y = octane

# 3-数据乱序
indices = np.random.permutation(len(X))
X = X[indices]
y = y[indices]

# 4-切分数据（保留最后20%作为测试集）
test_size = int(len(X)*0.2)
X_train, X_test = X[:-test_size], X[-test_size:]
y_train, y_test = y[:-test_size], y[-test_size:]

# 5-数据预处理（标准化）
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 转换为TensorFlow张量
X_train = tf.convert_to_tensor(X_train, dtype=tf.float32)
X_test = tf.convert_to_tensor(X_test, dtype=tf.float32)
y_train = tf.convert_to_tensor(y_train, dtype=tf.float32)
y_test = tf.convert_to_tensor(y_test, dtype=tf.float32)

# 6-建立回归模型
model = Sequential([
    Dense(64, activation='relu', kernel_regularizer='l2', input_shape=(401,)),
    Dropout(0.3),
    Dense(32, activation='relu', kernel_regularizer='l2'),
    Dropout(0.2),
    Dense(1)  # 输出层不需要激活函数
])

# 7-编译模型
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='mse',  # 回归任务使用均方误差
              metrics=['mae'])  # 监控平均绝对误差

# 8-训练模型（添加早停法）
early_stop = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

history = model.fit(X_train, y_train,
                    epochs=1000,
                    batch_size=8,
                    validation_split=0.2,
                    callbacks=[early_stop],
                    verbose=1)

# 9-可视化训练过程
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('MAE Curve')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend()

plt.tight_layout()
plt.show()

# 10-模型评估
y_pred = model.predict(X_test).flatten()

# 计算评价指标
mape = mean_absolute_percentage_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n模型性能评价:")
print(f"测试集相对误差（MAPE）: {mape:.4f}")
print(f"决定系数 R²: {r2:.4f}")

# 11-预测结果可视化
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
plt.xlabel('True Octane Value')
plt.ylabel('Predicted Octane Value')
plt.title('True vs Predicted Values')
plt.show()