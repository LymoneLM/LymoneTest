import numpy as np
import matplotlib.pyplot as plt

def free_fall(y0, t):
    if np.any(t < 0):
        raise ValueError("Time must be non-negative")
    g = -9.81
    v = g * t
    y = y0 + 0.5 * g * t**2
    return v, y

t = np.arange(0, 10.1, 0.1)
v, y = free_fall(20, t)

plt.plot(t, v, label='Velocity')
plt.plot(t, y, label='Distance')
plt.legend()
plt.title('Free Fall')
plt.xlabel('Time (s)')
plt.grid()
plt.show()
