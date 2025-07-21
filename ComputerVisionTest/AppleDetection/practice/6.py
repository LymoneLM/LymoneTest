import cv2
import numpy as np

# === 1. 加载图像 ===
img = cv2.imread("../data/chopsticks.png")
scale = 0.4
img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

# === 2. 灰度化 ===
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# === 3. 锐化增强边缘 ===
kernel_sharpen = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
gray = cv2.filter2D(gray, -1, kernel_sharpen)

# === 4. 中值模糊（去除斑点）===
gray = cv2.medianBlur(gray, 3)  # 可尝试 5 视情况调整

# === 5. 二值化（含反转）===
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
binary = 255 - binary  # 反转前景/背景

# === 6. 闭运算（填补小孔/连接）===
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# === 7. 再次模糊，用于平滑圆检测 ===
img_blur = cv2.GaussianBlur(gray, (5, 5), 1.2)

# === 8. Hough 圆检测 ===
circles = cv2.HoughCircles(
    img_blur,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=10,
    param1=50,
    param2=18,
    minRadius=3,
    maxRadius=12
)

# === 9. 绘制检测结果 ===
output = img.copy()
centers = []

if circles is not None:
    for (cx, cy, r) in np.uint16(np.around(circles[0])):
        centers.append((cx, cy))
        cv2.circle(output, (cx, cy), r, (0, 255, 0), 1)

# === 10. 去重中心点（合并靠得近的）===
def deduplicate_centers(centers, dist_thresh=8):
    if len(centers) == 0:
        return []
    centers = np.array(centers)
    kept = []
    used = np.zeros(len(centers), dtype=bool)
    for i in range(len(centers)):
        if not used[i]:
            dists = np.linalg.norm(centers - centers[i], axis=1)
            close = dists < dist_thresh
            mean_center = centers[close].mean(axis=0)
            kept.append(mean_center)
            used[close] = True
    return np.array(kept)

final_centers = deduplicate_centers(centers)

# === 11. 标号中心点 ===
for i, (x, y) in enumerate(final_centers):
    cv2.putText(output, str(i + 1), (int(x) - 4, int(y) + 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

print(f"最终检测到竹签数：{len(final_centers)}")
cv2.imshow("Detected Circles", output)
cv2.imwrite("output.png", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
