import cv2
import numpy as np


def calculate_psnr(img1, img2):
    """
    计算两张图片的峰值信噪比

    参数:
        img1 (numpy.ndarray): 第一张图片
        img2 (numpy.ndarray): 第二张图片

    返回:
        float: 峰值信噪比
    """
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def main():
    # 定义原始图片的路径
    original_image_paths = ["cropped1_1.jpg", "cropped1_2.jpg", "cropped1_3.jpg"]
    # 定义增强后图片的路径
    enhanced_image_paths = [
        "cropped2_1.jpg", "cropped2_2.jpg", "cropped2_3.jpg",
        "cropped3_1.jpg", "cropped3_2.jpg", "cropped3_3.jpg",
        "cropped4_1.jpg", "cropped4_2.jpg", "cropped4_3.jpg"
    ]

    try:
        for i, original_path in enumerate(original_image_paths):
            # 读取原始图片
            original_img = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
            if original_img is None:
                raise ValueError(f"无法读取原始图片: {original_path}")

            # 计算与该原始图片对应的 3 张增强后图片的 PSNR
            for j in range(3):
                enhanced_index = j * 3 + i
                if enhanced_index >= len(enhanced_image_paths):
                    break
                enhanced_path = enhanced_image_paths[enhanced_index]
                enhanced_img = cv2.imread(enhanced_path, cv2.IMREAD_GRAYSCALE)
                if enhanced_img is None:
                    print(f"无法读取增强后图片: {enhanced_path}")
                    continue

                # 计算 PSNR
                psnr = calculate_psnr(original_img, enhanced_img)
                print(f"增强后图片 {enhanced_path} 与原始图片 {original_path} 的 PSNR 值为: {psnr} dB")

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


if __name__ == "__main__":
    main()
