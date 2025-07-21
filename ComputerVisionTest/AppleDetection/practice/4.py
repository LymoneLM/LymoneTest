import cv2
import numpy as np
import os

# 输入输出路径
input_dir = '../data'
output_dir = '../results'

# 确保输出文件夹存在
os.makedirs(output_dir, exist_ok=True)

# 文件名列表
img_names = ['h1.png', 'h2.png', 'h3.png', 'h4.png', 'h5.png']

# 内部去噪函数（可用中值滤波）
def internal_denoise(img):
    return cv2.medianBlur(img, 5)

for idx, img_name in enumerate(img_names):
    input_path = os.path.join(input_dir, img_name)
    output_path = os.path.join(output_dir, f'{img_name}_morph.jpg')
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f'未找到图片: {input_path}，已跳过。')
        continue
    # 反色
    img_inv = cv2.bitwise_not(img)
    # 内部去噪
    img_proc = internal_denoise(img_inv)

    if idx == 0:
        # 1. 内部去噪-腐蚀-开运算
        img_proc = cv2.erode(img_proc, np.ones((3,3), np.uint8), iterations=1)
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    elif idx in [1, 2]:
        # 2/3. 内部去噪-开运算-8*8闭运算-10*10闭运算-6*6闭运算
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_CLOSE, np.ones((8,8), np.uint8))
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_CLOSE, np.ones((10,10), np.uint8))
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_CLOSE, np.ones((6,6), np.uint8))
    elif idx == 3:
        # 4. 内部去噪-开运算去除外部噪点
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_OPEN, np.ones((7,7), np.uint8))
    elif idx == 4:
        # 5. 内部去噪-闭运算修复破损
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8))
    # 反色回来
    result = cv2.bitwise_not(img_proc)
    cv2.imwrite(output_path, result)
    print(f'{img_name} 已处理，结果保存为 {output_path}')

print('全部处理完成，结果已保存到 results 文件夹。')
