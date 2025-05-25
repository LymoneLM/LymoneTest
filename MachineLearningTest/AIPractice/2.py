import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from matplotlib.colors import ListedColormap

# 生成二维网格数据
interval = 0.1
side = 1.5
x1 = np.arange(-side, side + interval, interval)
x2 = np.arange(-side, side + interval, interval)
xx1, xx2 = np.meshgrid(x1, x2)

# 计算目标函数值（二维网格形式）
F = (20
     + xx1 ** 2 - 10 * np.cos(2 * np.pi * xx1)
     + xx2 ** 2 - 10 * np.cos(2 * np.pi * xx2))

# 将网格数据展平为二维数组
X = np.column_stack([xx1.ravel(), xx2.ravel()])
F = F.ravel()  # 目标值展平为一维数组
# 为BP提供数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================== RBF网络部分 ==================
# ->精确RBF<-
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

# ->近似RBF网络<-
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

# ================== BP神经网络部分 ==================
bp_net = MLPRegressor(
    hidden_layer_sizes=(100, 100),
    activation='relu',
    solver='adam',
    max_iter=2000,
    random_state=42
)
bp_net.fit(X_scaled, F)
ty_bp = bp_net.predict(X_scaled)

# ================== 输出&可视化 ==================
# ================== 统一空间可视化 ==================
plt.rc("font", family='Microsoft YaHei', weight="bold")
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 设置各曲面的可视化参数
surf_params = [
    {"surface": F.reshape(xx1.shape), "cmap": 'viridis', "label": "原始函数", "alpha": 0.4},
    {"surface": ty_exact.reshape(xx1.shape), "cmap": 'plasma', "label": "精确RBF", "alpha": 0.6},
    {"surface": ty_approx.reshape(xx1.shape), "cmap": 'magma', "label": "近似RBF", "alpha": 0.7},
    {"surface": ty_bp.reshape(xx1.shape), "cmap": 'coolwarm', "label": "BP网络", "alpha": 0.7}
]


# 创建自定义半透明色带
def make_alpha_cmap(base_cmap, alpha=0.5):
    base_cmap = plt.get_cmap(base_cmap)
    color_list = base_cmap(np.arange(base_cmap.N))
    color_list[:, -1] = alpha  # 修改alpha通道
    return ListedColormap(color_list)


# 绘制各曲面
for param in surf_params:
    cmap = make_alpha_cmap(param["cmap"], param["alpha"])
    surf = ax.plot_surface(xx1, xx2, param["surface"],
                           cmap=cmap,
                           # rstride=2, cstride=2,  # 降低网格密度
                           edgecolor='k', linewidth=0.1,
                           label=param["label"])

# 添加图例代理
proxy_artists = [plt.Rectangle((0, 0), 1, 1, fc=plt.get_cmap(p["cmap"])(0.5), alpha=p["alpha"])
                 for p in surf_params]
ax.legend(proxy_artists, [p["label"] for p in surf_params],
          loc='upper left', bbox_to_anchor=(0.02, 0.95))

# 设置观察角度
ax.view_init(elev=38, azim=-135)

# 添加坐标轴设置
ax.set_xlabel('x1', labelpad=12)
ax.set_ylabel('x2', labelpad=12)
ax.set_zlabel('F', labelpad=10)
ax.grid(True, alpha=0.3)

# 添加颜色条
mappable = plt.cm.ScalarMappable(cmap='viridis')
mappable.set_array(F)
cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
cbar.set_label('函数值范围', rotation=270, labelpad=15)

plt.tight_layout()
plt.show()


def print_metrics(name, true, pred):
    print(f"{name}:")
    print(f"MSE: {mean_squared_error(true, pred):.4f}")
    print(f"R²: {r2_score(true, pred):.4f}")


print_metrics("精确RBF", F, ty_exact)
print_metrics("近似RBF", F, ty_approx)
print_metrics("BP网络", F, ty_bp)
