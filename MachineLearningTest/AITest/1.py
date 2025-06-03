import numpy as np
from numpy.linalg import inv

Ln = 5000
std = 0
lamt = 1

a10 = 1
a20 = -0.6
b10 = -0.5
b20 = 0.4
Truec = np.zeros((1, 4))
Truec[0:, 0:] = [a10, a20, b10, b20]
y = np.zeros(Ln)
u = np.zeros(Ln)
nnoise = np.zeros(Ln)

for i in range(0, Ln):
    nnoise[i] = np.random.randn()
    u[i] = np.random.randn()

for k in range(0, Ln):
    y[k] = a10 * y[k - 1] + a20 * y[k - 2] + b10 * u[k - 1] + b20 * u[k - 2] + std * nnoise[k]

c0 = np.zeros((4, 1))
h1 = np.zeros((4, 1))
p0 = np.eye(4)
E = np.eye(4)
p0 = 1e10 * p0
c = np.zeros((4, Ln))

for k in range(2, Ln):
    h1[0:, 0] = [y[k - 1], y[k - 2], u[k - 1], u[k - 2]]

    m = inv(lamt + (h1.T).dot(p0).dot(h1))
    k1 = p0.dot(h1)
    k1 = k1.dot(m)

    new = y[k] - h1.T.dot(c0)

    c1 = c0 + k1.dot(new)

    p0 = 1 / lamt * (E - k1.dot(h1.T)).dot(p0)

    c[0:, k:k + 1] = c1
    c0 = c1
res = c1

Prec = res.T - Truec
Tpc = np.dot(Truec, Truec.T)
print(Tpc)
result = np.dot(Prec, Prec.T).dot((1 / Tpc))
print(Truec)
print(res.T)
print(result)
