import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams.update({
    'font.sans-serif': ['Microsoft YaHei'],
    'axes.unicode_minus': False
})

# 梁与载荷参数设定
length = 6.0               # 梁长 (m)
uniform_load = 10.0        # 均布载荷强度 (kN/m)
point_load_1 = 10.0        # 集中力1 (kN)
point_load_2 = -40.0       # 集中力2 (kN，向上为负)
load_pos_1 = 2.0           # P1 作用位置 (m)
load_pos_2 = 4.0           # P2 作用位置 (m)

# 计算支座反力
def calculate_supports(L, q, P1, P2, x1, x2):
    distributed = q * L
    total = distributed + P1 + P2
    moment_A = distributed * (L / 2) + P1 * x1 + P2 * x2
    RB = moment_A / L
    RA = total - RB
    return RA, RB

RA, RB = calculate_supports(length, uniform_load, point_load_1, point_load_2, load_pos_1, load_pos_2)

# 弯矩函数定义
def bending_moment(x_vals, R_left, q, P1, P2, x1, x2):
    results = []
    for x in x_vals:
        Mx = R_left * x
        if x >= x1:
            Mx -= P1 * (x - x1)
        if x >= x2:
            Mx -= P2 * (x - x2)
        Mx -= q * x**2 / 2
        results.append(Mx)
    return np.array(results)

# 生成计算点与绘图
positions = np.linspace(0, length, 500)
moment_values = bending_moment(positions, RA, uniform_load, point_load_1, point_load_2, load_pos_1, load_pos_2)

plt.figure(figsize=(10, 5))
plt.plot(positions, moment_values, label='弯矩分布', color='blue')
plt.axhline(0, color='gray', linewidth=0.8)
plt.title("简支梁的弯矩图")
plt.xlabel("位置 x (米)")
plt.ylabel("弯矩 M (kN·m)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()