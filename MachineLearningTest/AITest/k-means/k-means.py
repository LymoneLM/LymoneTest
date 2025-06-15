import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读数据
data = np.loadtxt('datapoints.txt')

# K-means聚类
k = 4
centroids, _ = kmeans(data, k)
cluster_labels, _ = vq(data, centroids)

# 绘制结果
plt.figure(figsize=(10, 6), dpi=100)
colors = ['#FF6B6B', '#4ECDC4', '#FFD166', '#6A4C93']
markers = ['o', 's', '^', 'D']
labels = ['桩基类型1', '桩基类型2', '桩基类型3', '桩基类型4']

for i in range(k):
    cluster_data = data[cluster_labels == i]
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                c=colors[i], marker=markers[i],
                s=50, alpha=0.85, edgecolors='w', linewidth=0.6,
                label=labels[i])

plt.scatter(centroids[:, 0], centroids[:, 1],
            s=200, c='#2A2B2E', marker='*',
            label='聚类中心', edgecolors='gold', linewidth=1.5, zorder=10)

plt.xlabel('承载力 (kN)', fontsize=12)
plt.ylabel('沉降量 (mm)', fontsize=12)
plt.title('桩基试验分类结果', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(loc='best', fontsize=10)

plt.gca().set_facecolor('#F5F5F5')
plt.tight_layout()

# 保存
plt.savefig('桩基分类结果.png', dpi=300, bbox_inches='tight')
plt.show()