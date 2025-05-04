import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['STSong']
plt.rcParams['font.size'] = 20
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False

# 初始化/生成数据
Ln = 1000
std = 0.1
lamt = 1
a10 = 0.8
a20 = -0.6
b10 = -0.5
b20 = 0.4
b30 = 0.3
Truec = np.zeros((1, 5))
Truec[0:, 0:] = [a10, a20, b10, b20, b30]
y = np.zeros(Ln)
u = np.zeros(Ln)
nnoise = np.zeros(Ln)
for i in range(0, Ln):
    nnoise[i] = np.random.randn() + 1
    u[i] = np.random.randn()
for k in range(0, Ln):
    y[k] = a10 * y[k - 1] + a20 * y[k - 2] + b10 * u[k - 1] + b20 * u[k - 2] + b30 * u[k - 3] + std * nnoise[k]

# 展示数据
plt.figure(figsize=(12, 6))
plt.plot(u, label='u')
plt.plot(y, label='y')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.title('查看数据')
plt.show()

# 在线最小二乘法
c0 = np.zeros((5, 1))
h1 = np.zeros((5, 1))
p0 = np.eye(5)
E = np.eye(5)
p0 = 1e10 * p0
c = np.zeros((5, Ln))

wc = np.zeros(Ln-2)  # 用于记录误差
for k in range(3, Ln):  # 最小二乘迭代
    h1[0:, 0] = [y[k - 1], y[k - 2], u[k - 1], u[k - 2], u[k - 3]]

    m = inv(lamt + (h1.T).dot(p0).dot(h1))
    k1 = p0.dot(h1)
    k1 = k1.dot(m)

    new = y[k] - h1.T.dot(c0)
    c1 = c0 + k1.dot(new)
    p0 = 1 / lamt * (E - k1.dot(h1.T)).dot(p0)

    c[0:, k:k + 1] = c1
    c0 = c1

    # 计算误差
    sum = 0
    yc = np.zeros(Ln)
    res = c1
    for ki in range(0, Ln):
        yc[ki] = res[0][0] * y[ki - 1] + res[1][0] * y[ki - 2] + res[2][0] * u[ki - 1] + res[3][0] * u[ki - 2] + res[4][0] * u[ki - 3]
        sum += (y[ki]-yc[ki])**2
    wc[k-3] = sum / 2

res = c1

Prec = res.T - Truec
Tpc = np.dot(Truec, Truec.T)
print(Tpc)
result = np.dot(Prec, Prec.T).dot((1 / Tpc))
print(Truec)
print(res.T)
print(result)

ye = np.zeros(Ln)
yc = np.zeros(Ln)
for k in range(0, Ln):
    yc[k] = a10 * y[k - 1] + a20 * y[k - 2] + b10 * u[k - 1] + b20 * u[k - 2] + b30 * u[k - 3]
    ye[k] = res[0][0] * y[k - 1] + res[1][0] * y[k - 2] + res[2][0] * u[k - 1] + res[3][0] * u[k - 2] + res[4][0] * u[k - 3]

# 绘制拟合曲线
plt.figure(figsize=(12, 6))
plt.plot(yc, label='原始')
plt.plot(ye, label='拟合')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.title('拟合曲线')
plt.show()

# 绘制误差曲线
plt.figure(figsize=(12, 6))
plt.plot(wc, label='平方误差')
plt.legend()
plt.title('误差曲线')
plt.show()

