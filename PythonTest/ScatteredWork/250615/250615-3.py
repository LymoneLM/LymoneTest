import numpy as np
import matplotlib.pyplot as plt

def freefall(y0, t):
    if (isinstance(t, (int, float)) and t < 0) or (isinstance(t, np.ndarray) and np.any(t < 0)):
        print("Time cannot be negative")
        return None, None
    g = -9.81
    v = g * t
    y = y0 + 0.5 * g * t**2
    return v, y

t_vals = np.arange(0, 10.1, 0.1)
y0 = 20
velocities, distances = freefall(y0, t_vals)

plt.figure(figsize=(10, 6))
plt.plot(t_vals, velocities, label='Velocity (m/s)')
plt.plot(t_vals, distances, label='Distance (m)')
plt.xlabel('Time (s)')
plt.ylabel('Value')
plt.title('Free Fall: Velocity and Distance vs Time')
plt.legend()
plt.grid(True)
plt.show()