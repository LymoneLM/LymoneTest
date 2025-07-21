import cv2
import numpy as np

# 读取图片
img = cv2.imread('input/4.jpg')

# 转灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 1. CLAHE提升对比度 + 中值滤波去斑点
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray_clahe = clahe.apply(gray)
gray_clahe = cv2.medianBlur(gray_clahe, 5)

# 1. Canny边缘检测
edges = cv2.Canny(gray_clahe, 50, 150)

# 1. 轮廓检测，筛选近似圆形
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
circle_contours = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 1000:
        continue
    perimeter = cv2.arcLength(cnt, True)
    if perimeter == 0:
        continue
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    if circularity > 0.6:  # 圆度阈值
        circle_contours.append(cnt)

# 2. 霍夫圆检测
circles = cv2.HoughCircles(
    gray_clahe, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
    param1=100, param2=30, minRadius=30, maxRadius=80
)

h, w = img.shape[:2]
margin = 30

# 3. 比较霍夫圆与轮廓的重叠度
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        x, y, r = int(i[0]), int(i[1]), int(i[2])
        if x < margin or x > w - margin or y < margin or y > h - margin:
            continue
        if r < 35 or r > 75:
            continue
        # 构造圆mask
        circle_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(circle_mask, (x, y), r, 255, -1)
        # 计算与所有圆形轮廓的最大重叠度
        max_overlap = 0
        for cnt in circle_contours:
            contour_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.drawContours(contour_mask, [cnt], -1, 255, -1)
            intersection = cv2.bitwise_and(circle_mask, contour_mask)
            union = cv2.bitwise_or(circle_mask, contour_mask)
            overlap = np.sum(intersection > 0) / np.sum(union > 0)
            if overlap > max_overlap:
                max_overlap = overlap
        print(f"圆心({x},{y}) 半径{r} 最大重叠度: {max_overlap:.2f}")
        if max_overlap > 0.3:  # 重叠度阈值，可调
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(img, (x - r, y - r), (x + r, y + r), (0, 128, 255), 2)

# 显示结果
cv2.imshow('CLAHE+Median', gray_clahe)
cv2.imshow('Edges', edges)
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
