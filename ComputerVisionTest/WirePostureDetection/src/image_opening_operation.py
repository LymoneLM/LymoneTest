import cv2
import numpy as np


def opening_operation(input_path, output_path):
    try:
        # 读取图像
        image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        # 定义长度为 8、角度为 0 的线性结构元素
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 1))
        # 进行开运算
        opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        # 保存处理后的图像
        cv2.imwrite(output_path, opened_image)
        print(f"处理后的图像已保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def get_opening_operation(input_img):
    # 定义长度为 8、角度为 0 的线性结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 1))
    # 进行开运算
    opened_image = cv2.morphologyEx(input_img, cv2.MORPH_OPEN, kernel)

    return opened_image



if __name__ == "__main__":
    input_image_path = '../output/output_gray.png'
    output_image_path = '../output/output_opening.png'
    opening_operation(input_image_path, output_image_path)
