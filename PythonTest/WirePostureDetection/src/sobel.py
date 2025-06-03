import cv2
import numpy as np
import matplotlib.pyplot as plt


def sobel_edge_detection(image_path, threshold):
    """
    使用Sobel算子进行边缘检测

    参数:
    image_path (str): 图像文件的路径
    threshold (int): 用于二值化的阈值

    返回:
    edges (numpy.ndarray): 边缘检测后的图像
    """
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("无法读取图像，请检查图像路径。")
        return None

    # 使用Sobel算子计算梯度
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # x方向梯度
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)  # y方向梯度

    # 计算梯度幅值
    gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)

    # 将梯度幅值归一化到0-255范围
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 使用阈值进行二值化
    _, edges = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)

    return edges

if __name__ == "__main__":
    # 示例使用
    image_path = '../output/rectified_left1_image.png'
    threshold = 100  # 二值化阈值，可以根据图像调整

    # 进行边缘检测
    edges = sobel_edge_detection(image_path, threshold)

    if edges is not None:
        # 显示原始图像和边缘检测结果
        plt.subplot(121), plt.imshow(cv2.imread(image_path), cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.show()

        # 保存边缘检测后的图像
        output_path = '../output/edge_detected_image_sobel.png'
        cv2.imwrite(output_path, edges)
        print(f"边缘检测后的图像已保存到 {output_path}")

        # 定义三个坐标正方形区域
        regions = [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)]

        for i, region in enumerate(regions):
            x1, y1, x2, y2 = region
            # 提取指定区域的图像
            region_image = edges[y1:y2, x1:x2]
            # 保存指定区域的图像
            region_output_path = f'edge_detected_sobel_image_region_{i + 1}.png'
            cv2.imwrite(region_output_path, region_image)
            print(f"区域 {i + 1} 的图像已保存到 {region_output_path}")