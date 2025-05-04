# 双sigmoid串联
import matplotlib.pyplot as plt
import numpy as np

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['STSong']
plt.rcParams['font.size'] = 20
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False

Mcz = 0.2
eta = 0.1  # 学习率
epoch = 1001
w1 = Mcz
b1 = -Mcz
w2 = Mcz
b2 = -Mcz
Xt = np.linspace(-np.pi, np.pi)
T = np.sin(0.6 * Xt) / 7 + np.sin(0.7 * Xt) / 5 + 0.5
n_data = len(T)


def sigmoid(x, w, b):  # sigmoid激活函数
    u = x * w + b
    return 1 / (1 + np.exp(-u))


def loss(Y, T):  # 损失函数
    return 1 / 2 * np.sum((Y - T) ** 2)


def forward(x, w1, b1, w2, b2):  # 正向传播，串联
    y1 = sigmoid(x, w1, b1)
    y2 = sigmoid(y1, w2, b2)  # 串联
    return y1, y2


def backward(x, y1, y2, t, w1, b1, w2, b2):  # 反向传播
    delta = (y2 - t) * (1 - y2) * y2  # delta2
    grad_w2 = y1 * delta
    grad_b2 = delta
    delta = delta * w2 * (1 - y1) * y1  # dleta1
    grad_w1 = x * delta
    grad_b1 = delta
    w1 -= eta * grad_w1
    b1 -= eta * grad_b1
    w2 -= eta * grad_w2
    b2 -= eta * grad_b2
    return w1, b1, w2, b2


def show_output(X, Y, T, epoch):
    plt.figure(num='fig1')
    plt.plot(X, T, color='r', linestyle='--', label='真实值')
    plt.scatter(X, Y, color='g', marker='+', label='单神经元预测值')
    plt.legend(loc='lower right', fontsize=20, ncol=1)
    plt.xlabel("x", size=30)
    plt.ylabel("y", size=30)
    plt.tick_params(labelsize=10)
    plt.grid()
    plt.show()
    print("Epoch:", epoch)
    print("Loss:", loss(Y, T))


for i in range(epoch):

    if i < epoch:
        Y1, Y = forward(Xt, w1, b1, w2, b2)
        if i % 200 == 0:
            show_output(Xt, Y, T, i)

    idx_rand = np.arange(n_data)  # 0 - N 生成数字
    np.random.shuffle(idx_rand)  # 随机打乱（如果顺序一定可能会对学习造成负面影响

    for j in idx_rand:
        x = Xt[j]
        t = T[j]
        y1, y2 = forward(x, w1, b1, w2, b2)
        w1, b1, w2, b2 = backward(x, y1, y2, t, w1, b1, w2, b2)

# 输出结果
Y1, Y = forward(Xt, w1, b1, w2, b2)
show_output(Xt, Y, T, epoch)

print(w1, b1, w2, b2)
