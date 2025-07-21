import cv2 as cv
import numpy as np

# 读取原图
img = cv.imread('../data/affine.png')

# 获取图像尺寸
rows, cols = img.shape[:2]

# 原图变换的顶点（请根据实际格子角点调整）
pts1 = np.float32([[50, 50], [400, 50], [50, 400]])
# 目标图像变换顶点（可根据需要调整）
pts2 = np.float32([[100, 100], [300, 50], [100, 400]])

# 构建仿射变换描述矩阵
M = cv.getAffineTransform(pts1, pts2)

# 进行仿射变换
dst = cv.warpAffine(img, M, (cols, rows))

# 保存结果
cv.imwrite('../results/affine.jpg', dst)

print('仿射变换完成，结果已保存为 results/affine.jpg')
