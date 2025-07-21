import cv2
import numpy as np
from scipy.spatial.distance import cdist

# 1. 加载图像
img = cv2.imread('../data/coin2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 二值化（OTSU）
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 3. 查找轮廓
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. 提取圆心点列表（过滤太小轮廓）
min_area = 50
centers = []
for cnt in contours:
    if cv2.contourArea(cnt) > min_area:
        (x, y), r = cv2.minEnclosingCircle(cnt)
        centers.append([x, y])

centers = np.array(centers)

# 5. 去除过于接近的圆心（合并重复）
# 两点间距离小于某个阈值视为同一硬币
def deduplicate_centers(centers, dist_thresh=10):
    if len(centers) == 0:
        return []
    kept = []
    used = np.zeros(len(centers), dtype=bool)
    for i in range(len(centers)):
        if not used[i]:
            dists = np.linalg.norm(centers - centers[i], axis=1)
            same_group = dists < dist_thresh
            mean_center = centers[same_group].mean(axis=0)
            kept.append(mean_center)
            used[same_group] = True
    return np.array(kept)

deduped_centers = deduplicate_centers(centers, dist_thresh=12)

# 6. 绘制并显示
output = img.copy()
for i, (x, y) in enumerate(deduped_centers):
    cv2.circle(output, (int(x), int(y)), 10, (0, 255, 0), 1)
    cv2.putText(output, f"{i+1}", (int(x)-6, int(y)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

print(f"检测到的硬币数：{len(deduped_centers)}")
cv2.imshow("Coins", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
