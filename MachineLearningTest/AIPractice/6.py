import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 读取数据
data = pd.read_csv('data/zgpa_train.csv')

# 日期转换
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 使用收盘价进行预测
close_prices = data['close'].values.reshape(-1, 1)

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_close = scaler.fit_transform(close_prices)

# 创建序列数据
def create_dataset(dataset, look_back=5):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:i + look_back, 0])
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)

look_back = 5
X, y = create_dataset(scaled_close, look_back)

# LSTM输入需要 [samples, time steps, features]
X = X.reshape((X.shape[0], X.shape[1], 1))

# 划分训练和测试集
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 构建LSTM模型
model = Sequential()
model.add(LSTM(50, return_sequences=False, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=1)

# 预测
y_pred = model.predict(X_test)
y_pred_inv = scaler.inverse_transform(y_pred.reshape(-1, 1))
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))

# 可视化
plt.figure(figsize=(10, 6))
plt.plot(y_test_inv, label='True Price')
plt.plot(y_pred_inv, label='Predicted Price')
plt.title('Stock Close Price Prediction with LSTM')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
