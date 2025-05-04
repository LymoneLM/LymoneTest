import matplotlib.pyplot as plt
import numpy as np

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['STSong']
plt.rcParams['font.size'] = 20
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False


Mcz = 0.2
eta = 0.1  # 学习率
epoch = 1001
w = Mcz
b = -Mcz
Xt = np.linspace(-np.pi, np.pi)
T = np.sin(0.6*Xt)/7+np.sin(0.7*Xt)/5+0.5
n_data = len(T)


# 正向传播
def forward(x, w, b):
    u = x * w + b
    y = 1 / (1 + np.exp(-u))
    return y


def backward(x, y, t):
    delta = (y - t) * (1 - y) * y
    grad_w = x * delta
    grad_b = delta
    return (grad_w, grad_b)


def show_output(X, Y, T, epoch):
    plt.figure(num='fig1')
    plt.plot(X, T,color='r', linestyle='--',label='真实值' )
    plt.scatter(X, Y, color='g', marker='+',label='单神经元预测值' )
    plt.legend(loc='lower right', fontsize=20, ncol=1)
    plt.xlabel("x", size=30)
    plt.ylabel("y", size=30)
    plt.tick_params(labelsize=10)
    plt.grid()
    plt.show()
    print("Epoch:", epoch)
    print("Error:", 1 / 2 * np.sum((Y - T) ** 2))


for i in range(epoch):

    if i < epoch:
        Y = forward(Xt, w, b)
        if i % 200 == 0:
            show_output(Xt, Y, T, i)

    idx_rand = np.arange(n_data)  # 0 - N 生成数字
    np.random.shuffle(idx_rand)  # 随机打乱（如果顺序一定可能会对学习造成负面影响

    for j in idx_rand:
        x = Xt[j]
        t = T[j]
        y = forward(x, w, b)
        grad_w, grad_b = backward(x, y, t)
        w -= eta * grad_w
        b -= eta * grad_b

Y = forward(Xt, w, b)
show_output(Xt, Y, T, epoch)


print(w)
print(b)