import cv2
import numpy as np

# ---------- 加载图像并预处理 ----------
img = cv2.imread("input/4.jpg")
resized = cv2.resize(img, (800, 800))
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# ---------- 颜色+亮度联合掩膜提取苹果 ----------
lower_red1 = np.array([0, 80, 80])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 80, 80])
upper_red2 = np.array([179, 255, 255])
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
fruit_mask = cv2.bitwise_or(mask1, mask2)

# 亮度约束 + 清除阴影
v_channel = hsv[:, :, 2]
bright_mask = cv2.inRange(v_channel, 100, 255)
combined_mask = cv2.bitwise_and(fruit_mask, bright_mask)

# 形态学处理消除小噪声
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
cleaned = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel, iterations=2)

# ---------- 轮廓提取 ----------
contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ---------- 处理每个水果区域 ----------
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 1500:
        continue

    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)

    roi = resized[y:y + h, x:x + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_mask = cv2.inRange(hsv_roi, np.array([0, 40, 40]), np.array([179, 255, 255]))

    # ---------- 成熟度判断（基于平均颜色） ----------
    mean_color = cv2.mean(roi, mask=roi_mask)
    bgr = np.array(mean_color[:3])[::-1]  # 转为BGR顺序
    if bgr[2] > 130 and bgr[1] < 100:
        ripeness = "Ripe"
    elif bgr[1] > 120:
        ripeness = "Unripe"
    else:
        ripeness = "Half-Ripe"

    # ---------- 缺陷检测（拉普拉斯纹理+边缘） ----------
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred_gray = cv2.GaussianBlur(roi_gray, (3, 3), 0)
    laplacian = cv2.Laplacian(blurred_gray, cv2.CV_64F)
    laplacian_abs = cv2.convertScaleAbs(laplacian)
    _, defect_mask = cv2.threshold(laplacian_abs, 25, 255, cv2.THRESH_BINARY)

    defect_contours, _ = cv2.findContours(defect_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defect_count = len([d for d in defect_contours if cv2.contourArea(d) > 20])

    # ---------- 信息标注 ----------
    label = f"{ripeness}, Defects: {defect_count}"
    cv2.putText(resized, label, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

# ---------- 显示和保存 ----------
cv2.imshow("Fruit Detection Result", resized)
cv2.imwrite("fruit_result_annotated.jpg", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
