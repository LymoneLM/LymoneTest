# 拟合非线性函数
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.optimizers import SGD


# 生成随机点
def Produce_Random_Data():
    global x_data, y_data
    # 生成x坐标
    x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
    #                                       增加一个维度

    # 生成噪声
    noise = np.random.normal(0, 0.02, x_data.shape)
    #                       均值 方差

    # 计算y坐标
    y_data = np.square(x_data) + noise

    # 画散点图
    plt.scatter(x_data, y_data)


# 神经网络拟合（训练及预测）
def Neural_Network():
    # 1 创建神经网络
    model = tf.keras.Sequential()

    # 添加层
    # 注：input_dim(输入神经元个数)只需要在输入层重视设置，后面的网络可以自动推断出该层的对应输入
    model.add(tf.keras.layers.Dense(units=5, input_dim=1, activation='tanh'))
    #                                   神经元个数  输入神经元个数 激活函数
    model.add(tf.keras.layers.Dense(units=1, activation='tanh'))
    #                               输出神经元个数

    # 2 设置优化器和损失函数
    model.compile(optimizer=SGD(0.3), loss='mse')
    #                 优化器     学习率     损失函数(均方误差)

    # 3 训练
    for i in range(3000):
        # 训练一次数据，返回loss
        loss = model.train_on_batch(x_data, y_data)

    # 4 预测
    y_pred = model.predict(x_data)

    # 5 画图
    plt.plot(x_data, y_pred, 'r-', lw=5)


# 1、生成随机点
Produce_Random_Data()

# 2、神经网络训练与预测
Neural_Network()

plt.show()