import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False # 解决坐标轴负号显示问题

# 1. 加载MATLAB数据文件
def load_traffic_data(file_path):
    """加载MATLAB格式的交通流量数据"""
    mat_data = loadmat(file_path)
    # 直接从MAT文件中提取训练和测试数据
    train_input = mat_data['input'].astype('float32')
    train_output = mat_data['output'].astype('float32')
    test_input = mat_data['input_test'].astype('float32')
    test_output = mat_data['output_test'].astype('float32')
    return train_input, train_output, test_input, test_output


# 2. 数据预处理
def preprocess_data(data, n_lags=4):
    """准备输入输出数据对，使用前n个时间点预测当前时间点"""
    X, y = [], []
    for i in range(n_lags, len(data)):
        X.append(data[i - n_lags:i])
        y.append(data[i])
    return np.array(X), np.array(y)


# 3. 小波激活函数（Morlet小波）
def wavelet_activation(x):
    """自定义小波激活函数"""
    return tf.math.cos(1.75 * x) * tf.math.exp(-tf.math.square(x) / 2)


# 4. 构建小波神经网络模型
def create_wavelet_nn(input_dim, hidden_units=12):
    """创建小波神经网络模型"""
    model = Sequential()

    # 输入层和隐含层（使用小波激活函数）
    model.add(Dense(hidden_units, input_dim=input_dim,
                    activation=wavelet_activation))

    # 输出层（线性激活函数用于回归问题）
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


# 主程序
def main():
    # 加载数据
    file_path = 'data/traffic_flux.mat'
    X_train, y_train, X_test, y_test = load_traffic_data(file_path)

    # 数据归一化
    scaler_input = MinMaxScaler(feature_range=(0, 1))
    scaler_output = MinMaxScaler(feature_range=(0, 1))

    # 训练数据归一化
    X_train_scaled = scaler_input.fit_transform(X_train)
    y_train_scaled = scaler_output.fit_transform(y_train)

    # 测试数据归一化（使用训练数据的归一化参数）
    X_test_scaled = scaler_input.transform(X_test)
    y_test_scaled = scaler_output.transform(y_test)

    # 创建并训练小波神经网络
    model = create_wavelet_nn(input_dim=X_train.shape[1])
    model.fit(X_train_scaled, y_train_scaled, epochs=200, batch_size=16, verbose=0)

    # 预测
    train_predict = model.predict(X_train_scaled)
    test_predict = model.predict(X_test_scaled)

    # 反归一化
    train_predict = scaler_output.inverse_transform(train_predict)
    y_train_actual = scaler_output.inverse_transform(y_train_scaled)
    test_predict = scaler_output.inverse_transform(test_predict)
    y_test_actual = scaler_output.inverse_transform(y_test_scaled)

    # 计算预测误差
    train_rmse = np.sqrt(np.mean((train_predict - y_train_actual) ** 2))
    test_rmse = np.sqrt(np.mean((test_predict - y_test_actual) ** 2))
    print(f"训练集RMSE: {train_rmse:.2f}")
    print(f"测试集RMSE: {test_rmse:.2f}")

    # 可视化结果
    plt.figure(figsize=(14, 8))

    # 训练集预测结果
    plt.subplot(2, 1, 1)
    plt.plot(y_train_actual, label='实际流量')
    plt.plot(train_predict, 'r--', label='预测流量')
    plt.title('训练集流量预测')
    plt.ylabel('交通流量')
    plt.legend()

    # 测试集预测结果
    plt.subplot(2, 1, 2)
    plt.plot(y_test_actual, label='实际流量')
    plt.plot(test_predict, 'r--', label='预测流量')
    plt.title('测试集流量预测')
    plt.xlabel('时间点')
    plt.ylabel('交通流量')
    plt.legend()

    plt.tight_layout()
    # plt.savefig('traffic_flux_prediction.png')
    plt.show()


if __name__ == "__main__":
    main()