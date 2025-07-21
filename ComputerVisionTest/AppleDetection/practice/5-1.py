import cv2
import numpy as np

# 1. 加载图像
img = cv2.imread('../data/coin1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. 对比度增强：自适应直方图均衡（CLAHE）
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray_enhanced = clahe.apply(gray)

# 3. 平滑处理（减噪）+ 保留边缘
blurred = cv2.GaussianBlur(gray_enhanced, (7, 7), 2)

# 4. 使用 HoughCircles 检测
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=20,         # 圆心最小间距（防止重叠）
    param1=50,          # Canny上限
    param2=25,          # 累加器阈值，越小越敏感（原来是30）
    minRadius=8,        # 根据图像调整
    maxRadius=30
)

# 5. 画图并打印
output = img.copy()
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i, (x, y, r) in enumerate(circles[0, :]):
        cv2.circle(output, (x, y), r, (0, 255, 0), 2)
        cv2.putText(output, f"{i+1}", (x - 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    print(f"强化后检测到硬币数量：{len(circles[0])}")
else:
    print("仍未检测到圆")

cv2.imshow("Enhanced Hough", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
