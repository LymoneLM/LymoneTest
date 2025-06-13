import numpy as np


# 目标函数
def objective_function(x):
    return 3 * np.cos(x[0] * x[1]) + x[0] + x[1] ** 2


# PSO参数设置
N = 100         # 粒子数量
D = 2           # 粒子维度
T = 200         # 最大迭代次数
c1 = c2 = 1.5   # 学习因子
w_max = 0.8     # 惯性权重最大值
w_min = 0.4     # 惯性权重最小值
x_max = 4.0     # 位置上限
x_min = -4.0    # 位置下限
v_max = 1.0     # 速度上限
v_min = -1.0    # 速度下限

# 初始化粒子位置和速度
np.random.seed(0)
positions = np.random.uniform(x_min, x_max, (N, D))
velocities = np.random.uniform(v_min, v_max, (N, D))

# 初始化个体最优位置和最优值
p_best_positions = positions.copy()
p_best_values = np.array([objective_function(p) for p in positions])

# 初始化全局最优位置和最优值
g_best_index = np.argmin(p_best_values)
g_best_position = p_best_positions[g_best_index].copy()
g_best_value = p_best_values[g_best_index]

# PSO主循环
for t in range(T):
    # 计算当前迭代的惯性权重（线性递减）
    w = w_max - (w_max - w_min) * (t / T)

    for i in range(N):
        # 更新速度
        r1, r2 = np.random.rand(2)
        velocities[i] = (w * velocities[i]
                         + c1 * r1 * (p_best_positions[i] - positions[i])
                         + c2 * r2 * (g_best_position - positions[i]))

        # 速度边界处理
        velocities[i] = np.clip(velocities[i], v_min, v_max)

        # 更新位置
        positions[i] += velocities[i]

        # 位置边界处理
        positions[i] = np.clip(positions[i], x_min, x_max)

        # 计算新位置的适应值
        current_value = objective_function(positions[i])

        # 更新个体最优
        if current_value < p_best_values[i]:
            p_best_values[i] = current_value
            p_best_positions[i] = positions[i].copy()

            # 更新全局最优
            if current_value < g_best_value:
                g_best_value = current_value
                g_best_position = positions[i].copy()

# 输出最终结果
print(f"找到的最小值: {g_best_value:.6f}")
print(f"最优解位置: x = {g_best_position[0]:.6f}, y = {g_best_position[1]:.6f}")