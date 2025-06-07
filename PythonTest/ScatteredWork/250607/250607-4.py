import numpy as np
import matplotlib.pyplot as plt
# 支持中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 梁参数
L = 6.0  # 梁长 m
q = 10.0  # 均布载荷 kN/m
P1 = 10.0  # 集中力1 kN
P2 = -40.0  # 集中力2 kN（向上）
a1 = 2.0  # P1 位置
a2 = 4.0  # P2 位置

# 反力计算
total_load = q * L + P1 + P2
moment_about_A = q * L * (L / 2) + P1 * a1 + P2 * a2
R2 = moment_about_A / L
R1 = total_load - R2

# 分段计算弯矩 M(x)
def moment(x):
    M = np.zeros_like(x)
    for i, xi in enumerate(x):
        m = R1 * xi
        if xi >= a1:
            m -= P1 * (xi - a1)
        if xi >= a2:
            m -= P2 * (xi - a2)
        m -= q * xi * (xi / 2)
        M[i] = m
    return M

# 生成位置点
x = np.linspace(0, L, 500)
Mx = moment(x)

# 绘图
plt.figure(figsize=(10, 5))
plt.plot(x, Mx, label='弯矩图 M(x)', color='b')
plt.axhline(0, color='black', linewidth=0.5)
plt.title("简支梁弯矩图")
plt.xlabel("梁长 x (m)")
plt.ylabel("弯矩 M (kN·m)")
plt.grid(True)
plt.legend()
plt.show()
