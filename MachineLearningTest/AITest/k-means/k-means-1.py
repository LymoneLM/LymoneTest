import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data_list = []
with open('datapoints.txt', 'r') as file:
    for line in file:
        values = line.strip().split()
        if len(values) == 2:
            data_list.append([float(values[0]), float(values[1])])
data = np.array(data_list)

centroids, _ = kmeans(data, 4)
cluster_labels, _ = vq(data, centroids)

plt.figure(figsize=(10, 6))
colors = ['red', 'green', 'blue', 'purple']
for i in range(4):
    cluster_data = data[cluster_labels == i]
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1], s=15, c=colors[i],
                label=f'类别 {i+1}')
plt.scatter(centroids[:, 0], centroids[:, 1], s=200, marker='*', c='black', label='聚类中心')
plt.xlabel('承载力 (kN)')
plt.ylabel('沉降量')
plt.title('桩基试验数据K-means聚类')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()