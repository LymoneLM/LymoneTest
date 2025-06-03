import cv2
import numpy as np

# 定义核函数
K1 = np.array([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
K2 = np.array([[-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
K3 = np.array([[-1, -1, -1], [1, 1, 1], [-1, -1, -1]])


def convolve_image(image, kernel):
    """
    对图像进行卷积操作
    :param image: 输入图像
    :param kernel: 卷积核
    :return: 卷积后的图像
    """
    height, width = image.shape
    kernel_height, kernel_width = kernel.shape
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
    result = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            patch = padded_image[y:y + kernel_height, x:x + kernel_width]
            result[y, x] = np.sum(patch * kernel)
    return result


def find_seed_points(image):
    """
    找到种子点
    :param image: 输入图像
    :return: 种子点坐标列表
    """
    response1 = convolve_image(image, K1)
    response2 = convolve_image(image, K2)
    response3 = convolve_image(image, K3)
    total_response = response1 + response2 + response3
    seed_points = np.argwhere(total_response == 3)
    return seed_points


def is_valid_point(x, y, height, width):
    """
    检查点是否在图像范围内
    :param x: 点的 x 坐标
    :param y: 点的 y 坐标
    :param height: 图像高度
    :param width: 图像宽度
    :return: 是否有效
    """
    return 0 <= x < width and 0 <= y < height


def get_neighbors(x, y):
    """
    获取像素点右侧 1、0、7 方向的邻域点
    :param x: 点的 x 坐标
    :param y: 点的 y 坐标
    :return: 邻域点列表
    """
    neighbors = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    return neighbors


def track_line(image, start_point, end_x):
    """
    从种子点开始跟踪线路
    :param image: 输入图像
    :param start_point: 种子点坐标
    :param end_x: 输电线右端点横坐标
    :return: 跟踪到的线路坐标列表
    """
    height, width = image.shape
    current_point = start_point
    line_points = [current_point]
    while current_point[0] < end_x:
        x, y = current_point
        neighbors = get_neighbors(x, y)
        valid_neighbors = []
        for nx, ny in neighbors:
            if is_valid_point(nx, ny, height, width):
                valid_neighbors.append((nx, ny))
        if len(valid_neighbors) == 0:
            break
        # 这里简单选择第一个有效邻域点作为下一个点，实际中可以根据线路走势选择
        next_point = valid_neighbors[0]
        line_points.append(next_point)
        current_point = next_point
    return line_points


def extract_transmission_line(image, left_endpoints, right_end_x):
    """
    提取输电线边界线的坐标
    :param image: 输入图像
    :param left_endpoints: 输电线边界线的左端点坐标列表
    :param right_end_x: 输电线右端点横坐标
    :return: 输电线边界线的坐标列表
    """
    all_lines = []
    for endpoint in left_endpoints:
        line = track_line(image, endpoint, right_end_x)
        all_lines.extend(line)
    return all_lines


# 示例使用
if __name__ == "__main__":
    # 读取图像（保持灰度图读取，后续转换为彩色图绘制标记）
    image_gray = cv2.imread('../output/edge_detected_image.png', cv2.IMREAD_GRAYSCALE)

    # 转换为彩色图像用于标注
    image_color = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)

    # 找到种子点
    seed_points = find_seed_points(image_gray)

    # 假设已知输电线边界线的左端点和右端点横坐标
    left_endpoints = [(0, 100), (0, 200)]  # 示例左端点坐标 (x, y) 格式
    right_end_x = 500  # 示例右端点横坐标

    # 提取输电线边界线的坐标（注意：track_line输入需要(y, x)格式，因为np.argwhere返回(y, x)）
    # 转换左端点格式为(y, x)（原假设的(x, y)需要交换顺序）
    left_endpoints_xy = [(y, x) for (x, y) in left_endpoints]  # 修正坐标顺序
    transmission_line_points = extract_transmission_line(image_gray, left_endpoints_xy, right_end_x)

    print("提取到的输电线边界线坐标（y, x格式）：", transmission_line_points)

    # 在彩色图像上标注特征点（转换为OpenCV的(x, y)坐标）
    for (y, x) in transmission_line_points:
        cv2.circle(image_color, (x, y), 3, (0, 0, 255), -1)  # 红色实心圆，半径3像素

    # 显示标注后的图像
    cv2.imshow('Transmission Line Points', image_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存标注后的图像
    cv2.imwrite('../output/line_points_marked.png', image_color)
    print("标注后的图像已保存为 line_points_marked.png")