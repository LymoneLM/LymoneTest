import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取真彩色图像
image_path = "img/1.jpg"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB格式

# 转换到HSV颜色空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)

# 增大亮度（V通道）为2倍，并限制最大值为255
hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * 2, 0, 255)

# 修改色调（H通道）和饱和度（S通道）
hsv_image[:, :, 0] = (hsv_image[:, :, 0] + 10) % 180  # 色调增加10
hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.2, 0, 255)  # 饱和度增加20%

# 转换回RGB颜色空间
hsv_image = hsv_image.astype(np.uint8)
processed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

# 显示原始图像和处理后的图像
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(image)
ax[0].set_title("Original Image")
ax[0].axis("off")

ax[1].imshow(processed_image)
ax[1].set_title("Processed Image")
ax[1].axis("off")

plt.show()
