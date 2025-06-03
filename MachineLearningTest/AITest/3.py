import numpy as np
import matplotlib.pyplot as plt


std = 0
Lnn = 100

X = np.linspace(-1, 3, Lnn)
T0 = X * X * X + 0.3 * X * X - 0.5 * X

Ln = len(T0)
Noisem = np.random.randn(Ln)
T = T0 + std * Noisem

eta = 0.001


def polynomial(x, params):
    poly = 0
    for i in range(len(params)):
        poly = poly + params[i] * x ** i
    return poly


def grad_params(X, T, params):
    grad_ps = np.zeros(len(params))
    for i in range(len(params)):
        for j in range(len(X)):
            grad_ps[i] += (polynomial(X[j], params) - T[j]) * pow(X[j], i)
    return grad_ps


def fit(X, T, degree, epoch):
    params = np.random.randn(degree + 1)
    for i in range(len(params)):
        params[i] *= 2 ** i
    for i in range(epoch):
        params -= eta * grad_params(X, T, params)
    return params


degree = 2
params = fit(X, T, degree, 1000)
Y = polynomial(X, params)
plt.scatter(X, T)
plt.plot(X, Y, 'r')
plt.show()

print((params))
