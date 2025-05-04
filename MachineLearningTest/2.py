"""
梯度下降算法
算法的目的是求出一个值，使得函数输出的值最小
"""
import numpy as np
import matplotlib.pyplot as plt

num = 50  # 迭代次数
theta = 10  # 初始节点
r = 0.1  # 学习率

Xresult = np.zeros(num)
Yresult = np.zeros(num)


# 求导函数
def dJ(theta):
    return 2 * theta + 2


# 原函数
def J(theta):
    return theta * theta + 2 * theta


for i in range(0, num):
    theta = theta - r * dJ(theta)
    Xresult[i] = theta
    Yresult[i] = J(Xresult[i])
    if i % 10 == 0:
        print("迭代次数[%d] 对应x的值 %.2f" % (i, theta))

print(Xresult)

plt.plot(Yresult, 'r:')
plt.axis([0, 50, -10, 100])
plt.tick_params(labelsize=10)

plt.show()
