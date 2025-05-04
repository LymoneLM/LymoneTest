import numpy as np
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['STSong']
plt.rcParams['font.size'] = 20
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False

# 使用提供的代码生成数据
Ln = 1000
std = 0.1
a10 = 0.8
a20 = -0.6
b10 = -0.5
b20 = 0.4
b30 = 0.3
y = np.zeros(Ln)
u = np.zeros(Ln)
nnoise = np.zeros(Ln)
for i in range(0, Ln):
    nnoise[i] = np.random.randn() + 1
    u[i] = np.random.randn()
for k in range(0, Ln):
    y[k] = a10 * y[k - 1] + a20 * y[k - 2] + b10 * u[k - 1] + b20 * u[k - 2] + b30 * u[k - 3] + std * nnoise[k]

# 拟合线性函数
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.optimizers import SGD

x_data = u
y_data = y

loss = np.zeros(3000)
# 创建神经网络（训练及预测）
def Neural_Network():
    # 创建神经网络
    model = tf.keras.Sequential()

    # 添加层
    model.add(tf.keras.layers.Dense(units=10, input_dim=1, activation='tanh'))
    model.add(tf.keras.layers.Dense(units=10, activation='tanh'))
    model.add(tf.keras.layers.Dense(units=10, activation='tanh'))
    model.add(tf.keras.layers.Dense(units=1, activation='tanh'))

    # 设置优化器和损失函数
    model.compile(optimizer=SGD(0.3), loss='mse')
    #                 优化器     学习率

    # 训练
    for i in range(3000):
        # 训练一次数据，返回loss
        loss[i] = model.train_on_batch(x_data, y_data)

    # 预测
    y_pred = model.predict(x_data)

    # 绘制拟合曲线
    plt.figure(figsize=(12, 6))
    plt.plot(y, label='原始')
    plt.plot(y_pred, label='拟合')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.title('拟合曲线')
    plt.show()


    plt.plot(loss, label='平方误差')
    plt.title('误差曲线')
    plt.legend()
    plt.show()



# 神经网络训练与预测
Neural_Network()


