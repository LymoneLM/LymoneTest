import numpy as np
import matplotlib.pyplot as plt

def func_g(x):
    return 0.5 * (np.exp(2 * x) - np.exp(-2 * x))

def func_h(x):
    ex2 = np.exp(2 * x)
    e_minus_2x = np.exp(-2 * x)
    return (ex2 - e_minus_2x) / (ex2 + e_minus_2x)

x_vals = np.linspace(-5, 5, 400)
plt.plot(x_vals, func_g(x_vals), label='g(x)')
plt.plot(x_vals, func_h(x_vals), label='h(x)')
plt.legend()
plt.title('g(x) and h(x)')
plt.grid()
plt.show()
