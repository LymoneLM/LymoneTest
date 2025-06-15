import numpy as np
from scipy.cluster.vq import kmeans, vq
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = np.loadtxt('datapoints.txt')
centroids, _ = kmeans(data, 4)
labels, _ = vq(data, centroids)

plt.figure(figsize=(10, 6))
colors = ['coral', 'limegreen', 'royalblue', 'darkviolet']
markers = ['s', '^', 'o', 'd']

for i in range(4):
    cluster_data = data[labels == i]
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                c=colors[i], marker=markers[i],
                label=f'桩基类型 {i+1}', alpha=0.7)

plt.scatter(centroids[:, 0], centroids[:, 1],
            s=200, c='gold', marker='*', edgecolor='black',
            linewidth=1, label='聚类中心')

plt.xlabel('承载力 (kN)', fontsize=12)
plt.ylabel('沉降量', fontsize=12)
plt.title('桩基聚类', fontsize=14)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()