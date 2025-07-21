import cv2
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei'] # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False # 正常显示负号

# 读取原图（灰度模式）
img = cv2.imread('../data/bkrc.png', cv2.IMREAD_GRAYSCALE)

# 定义3x3卷积核
kernel = np.ones((5, 5), np.uint8)

# 原图处理
eroded = cv2.erode(img, kernel, iterations=2)
dilated = cv2.dilate(eroded, kernel, iterations=4)

# 反色图像处理
img_inv = cv2.bitwise_not(img)
eroded_inv = cv2.erode(img_inv, kernel, iterations=2)
dilated_inv = cv2.dilate(eroded_inv, kernel, iterations=4)

# 展示
titles = [
    '原图', '腐蚀2次', '膨胀4次',
    '反色图', '反色腐蚀2次', '反色膨胀4次'
]
images = [img, eroded, dilated, img_inv, eroded_inv, dilated_inv]

plt.figure(figsize=(10, 8))
for i in range(3):
    plt.subplot(3, 2, 2*i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
    plt.subplot(3, 2, 2*i+2)
    plt.imshow(images[i+3], cmap='gray')
    plt.title(titles[i+3])
    plt.axis('off')

plt.tight_layout()
plt.show()