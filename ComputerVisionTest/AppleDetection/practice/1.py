import cv2

# 读取灰度图像
img = cv2.imread('../data/threshold.png', cv2.IMREAD_GRAYSCALE)

# 阈值
thresh = 127
maxval = 255

# 1. 二进制阈值分割
ret, binary = cv2.threshold(img, thresh, maxval, cv2.THRESH_BINARY)
cv2.imwrite('../results/binary.jpg', binary)

# 2. 反二进制阈值分割
ret, binary_inv = cv2.threshold(img, thresh, maxval, cv2.THRESH_BINARY_INV)
cv2.imwrite('../results/binary_inv.jpg', binary_inv)

# 3. 截断阈值
ret, trunc = cv2.threshold(img, thresh, maxval, cv2.THRESH_TRUNC)
cv2.imwrite('../results/trunc.jpg', trunc)

# 4. 阈值为零
ret, tozero = cv2.threshold(img, thresh, maxval, cv2.THRESH_TOZERO)
cv2.imwrite('../results/tozero.jpg', tozero)

# 5. 倒置阈值为零
ret, tozero_inv = cv2.threshold(img, thresh, maxval, cv2.THRESH_TOZERO_INV)
cv2.imwrite('../results/tozero_inv.jpg', tozero_inv)

# 6. 大津法自动阈值分割
ret2, otsu = cv2.threshold(img, 0, maxval, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite('../results/otsu.jpg', otsu)

print("阈值分割完成，结果已保存到 results 文件夹。")
