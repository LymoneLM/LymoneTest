import numpy as np

force = np.array([11, 7, 8, 10, 9])
k = np.array([1000, 600, 900, 1300, 700])

x = force / k
energy = k * x**2

a = [round(float(val), 6) for val in x]
b = [round(float(val), 6) for val in energy]

print("(a) Compressions / m:", a)
print("(b) Potential Energies / J:", b)