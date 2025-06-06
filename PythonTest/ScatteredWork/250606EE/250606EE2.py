import numpy as np
import matplotlib.pyplot as plt

k0 = 1200  # min^-1
Q = 8000   # cal/mol
R = 1.987  # cal/(mol·K)

temperatures = np.arange(100, 501, 50)

k_values = k0 * np.exp(-Q / (R * temperatures))

plt.figure(figsize=(10, 6))
plt.plot(temperatures, k_values, 'bo-', linewidth=2, markersize=8)
plt.title('Reaction Rate Constant vs Temperature')
plt.xlabel('Temperature (K)')
plt.ylabel('Rate Constant k (min⁻¹)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.yscale('log')
plt.tight_layout()

plt.show()