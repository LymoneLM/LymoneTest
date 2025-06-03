import cv2
import numpy as np
import matplotlib.pyplot as plt


def canny_edge_detection(image_path, low_threshold, high_threshold):
    """
    使用Canny算子进行边缘检测

    参数:
    image_path (str): 图像文件的路径
    low_threshold (int): Canny算子的低阈值
    high_threshold (int): Canny算子的高阈值

    返回:
    edges (numpy.ndarray): 边缘检测后的图像
    """
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("无法读取图像，请检查图像路径。")
        return None

    # 使用Canny算子进行边缘检测
    edges = cv2.Canny(image, low_threshold, high_threshold)

    return edges

def get_canny_edge_detection(input_img, low_threshold = 12, high_threshold = 150):
    edges = cv2.Canny(input_img, low_threshold, high_threshold)
    return edges



if __name__ == "__main__":
    # 示例使用
    image_path = '../output/rectified_left1_image.png'
    low_threshold = 12
    high_threshold = 150

    # 进行边缘检测
    edges = canny_edge_detection(image_path, low_threshold, high_threshold)

    if edges is not None:
        # 显示原始图像和边缘检测结果
        plt.subplot(121), plt.imshow(cv2.imread(image_path), cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.show()

        # 保存边缘检测后的图像
        output_path = '../output/edge_detected_image.png'
        cv2.imwrite(output_path, edges)
        print(f"边缘检测后的图像已保存到 {output_path}")

        # 定义三个坐标正方形区域
        regions = [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)]

        for i, region in enumerate(regions):
            x1, y1, x2, y2 = region
            # 提取指定区域的图像
            region_image = edges[y1:y2, x1:x2]
            # 保存指定区域的图像
            region_output_path = f'../output/edge_detected_image_region_{i + 1}.png'
            cv2.imwrite(region_output_path, region_image)
            print(f"区域 {i + 1} 的图像已保存到 {region_output_path}")
