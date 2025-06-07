import numpy as np
import matplotlib.pyplot as plt

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 梁参数配置
beam_len = 6.0
q_load = 10.0
f1 = 10.0
f2 = -40.0
x_f1 = 2.0
x_f2 = 4.0

# 支座反力求解函数
def support_reactions(L, q, F1, F2, pos1, pos2):
    eq_force = q * L + F1 + F2
    moment_O = q * L * L / 2 + F1 * pos1 + F2 * pos2
    Rb = moment_O / L
    Ra = eq_force - Rb
    return Ra, Rb

Ra_val, Rb_val = support_reactions(beam_len, q_load, f1, f2, x_f1, x_f2)

# 弯矩值计算器
def compute_bending(x_array, Ra, q, F1, F2, p1, p2):
    def moment_at(x):
        M = Ra * x
        M -= F1 * max(0, x - p1)
        M -= F2 * max(0, x - p2)
        M -= q * x**2 / 2
        return M
    return np.array([moment_at(xi) for xi in x_array])

# 离散位置与绘图
x_range = np.linspace(0, beam_len, 600)
M_values = compute_bending(x_range, Ra_val, q_load, f1, f2, x_f1, x_f2)

plt.figure(figsize=(9, 4.5))
plt.plot(x_range, M_values, 'b-', label='M(x) 弯矩')
plt.axhline(0, color='black', lw=0.7)
plt.title('弯矩图（简支梁）')
plt.xlabel('位置 x (m)')
plt.ylabel('弯矩值 M (kN·m)')
plt.grid(alpha=0.4)
plt.legend()
plt.show()