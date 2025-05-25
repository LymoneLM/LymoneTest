import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score

# 生成数据
interval = 0.01
x1 = np.linspace(-1.5, 1.5, int(3 / interval) + 1)
x2 = np.linspace(-1.5, 1.5, int(3 / interval) + 1)

# 计算目标函数值
F = 20 + x1**2 - 10 * np.cos(2 * np.pi * x1) + x2**2 - 10 * np.cos(2 * np.pi * x2)

# 构造输入数据 (2, 301)
X = np.vstack([x1, x2]).T  # (301, 2)

# 精确RBF网络
# 计算自适应spread参数
dists = euclidean_distances(X)
triu_indices = np.triu_indices_from(dists, k=1)
mean_dist = np.mean(dists[triu_indices])
gamma_exact = 1 / (2 * (mean_dist ** 2))

# 构造RBF特征矩阵
Phi_exact = rbf_kernel(X, X, gamma=gamma_exact)

# 求解权重
w_exact, _, _, _ = np.linalg.lstsq(Phi_exact, F, rcond=None)
ty_exact = Phi_exact.dot(w_exact)

# 近似RBF网络
n_centers = 50  # 聚类中心数
kmeans = KMeans(n_clusters=n_centers)
kmeans.fit(X)
centers = kmeans.cluster_centers_

# 计算近似模型的gamma
dists_approx = euclidean_distances(centers)
triu_indices_approx = np.triu_indices_from(dists_approx, k=1)
mean_dist_approx = np.mean(dists_approx[triu_indices_approx])
gamma_approx = 1 / (2 * (mean_dist_approx ** 2))

# 构造近似RBF特征矩阵
Phi_approx = rbf_kernel(X, centers, gamma=gamma_approx)

# 求解权重
w_approx, _, _, _ = np.linalg.lstsq(Phi_approx, F, rcond=None)
ty_approx = Phi_approx.dot(w_approx)

# 可视化结果
plt.rc("font",family='MicroSoft YaHei',weight="bold")
fig = plt.figure(figsize=(12, 6))

# 精确RBF可视化
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(x1, x2, F, c='r', marker='o', label='真实值')
ax1.scatter(x1, x2, ty_exact, c='b', linestyle='-.', label='预测值')
ax1.view_init(elev=36, azim=113)
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.set_zlabel('F')
ax1.set_title('精确RBF网络拟合效果')

# 近似RBF可视化
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(x1, x2, F, c='r', marker='o', label='真实值')
ax2.scatter(x1, x2, ty_approx, c='g', linestyle='-.', label='预测值')
ax2.view_init(elev=36, azim=113)
ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.set_zlabel('F')
ax2.set_title('近似RBF网络拟合效果')

plt.tight_layout()
plt.show()

# 评估指标
print("精确RBF网络:")
print(f'MSE: {mean_squared_error(F, ty_exact):.4e}')
print(f'R²: {r2_score(F, ty_exact):.4f}\n')

print("近似RBF网络:")
print(f'MSE: {mean_squared_error(F, ty_approx):.4e}')
print(f'R²: {r2_score(F, ty_approx):.4f}')