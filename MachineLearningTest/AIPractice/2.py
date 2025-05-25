import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score

# 生成二维网格数据
interval = 0.1
x1 = np.arange(-1.5, 1.5+interval, interval)
x2 = np.arange(-1.5, 1.5+interval, interval)
xx1, xx2 = np.meshgrid(x1, x2)

# 计算目标函数值（二维网格形式）
F = (20
     + xx1**2 - 10*np.cos(2*np.pi*xx1)
     + xx2**2 - 10*np.cos(2*np.pi*xx2))

# 将网格数据展平为二维数组
X = np.column_stack([xx1.ravel(), xx2.ravel()])
F = F.ravel()  # 目标值展平为一维数组

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
# 精确RBF可视化
fig = plt.figure(figsize=(15,6))

# 原始曲面
ax1 = fig.add_subplot(131, projection='3d')
surf1 = ax1.plot_surface(xx1, xx2, F.reshape(xx1.shape),
                       cmap='viridis', alpha=0.8)
ax1.set_title("原始函数曲面")

# 精确RBF预测结果
ax2 = fig.add_subplot(132, projection='3d')
surf2 = ax2.plot_surface(xx1, xx2, ty_exact.reshape(xx1.shape),
                       cmap='plasma', alpha=0.8)
ax2.set_title("精确RBF拟合曲面")

# 近似RBF预测结果
ax3 = fig.add_subplot(133, projection='3d')
surf3 = ax3.plot_surface(xx1, xx2, ty_approx.reshape(xx1.shape),
                       cmap='magma', alpha=0.8)
ax3.set_title("近似RBF拟合曲面")

plt.tight_layout()
plt.show()

# 评估指标
print("精确RBF网络:")
print(f'MSE: {mean_squared_error(F, ty_exact):.4e}')
print(f'R²: {r2_score(F, ty_exact):.4f}\n')

print("近似RBF网络:")
print(f'MSE: {mean_squared_error(F, ty_approx):.4e}')
print(f'R²: {r2_score(F, ty_approx):.4f}')