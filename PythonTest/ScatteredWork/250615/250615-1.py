import numpy as np
import matplotlib.pyplot as plt

def g(x):
    return (np.exp(2*x) - np.exp(-2*x)) / 2

def h(x):
    return (np.exp(2*x) - np.exp(-2*x)) / (np.exp(2*x) + np.exp(-2*x))

x = np.linspace(-5, 5, 400)
g_values = g(x)
h_values = h(x)

plt.figure(figsize=(10, 6))
plt.plot(x, g_values, label='$g(x) = \\frac{e^{2x} - e^{-2x}}{2}$')
plt.plot(x, h_values, label='$h(x) = \\frac{e^{2x} - e^{-2x}}{e^{2x} + e^{-2x}}$')
plt.xlabel('x')
plt.ylabel('Function Value')
plt.title('Function Plots')
plt.legend()
plt.grid(True)
plt.ylim(-5, 5)
plt.show()