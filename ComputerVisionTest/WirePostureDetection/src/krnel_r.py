import cv2
import numpy as np

# 定义核函数（保持不变）
K1 = np.array([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
K2 = np.array([[-1, -1, 1], [-1, 1, -1], [1, -1, -1]])
K3 = np.array([[-1, -1, -1], [1, 1, 1], [-1, -1, -1]])


def convolve_image(image, kernel):
    """优化卷积操作（使用OpenCV）"""
    return cv2.filter2D(image, -1, kernel, borderType=cv2.BORDER_REPLICATE)


def find_seed_points(image):
    """找到种子点（返回(x, y)格式）"""
    response1 = convolve_image(image, K1)
    response2 = convolve_image(image, K2)
    response3 = convolve_image(image, K3)
    total_response = response1 + response2 + response3

    # 获取响应值为3的点并转换为(x, y)格式
    seed_points = []
    ys, xs = np.where(total_response == 3)
    for x, y in zip(xs, ys):
        seed_points.append((x, y))
    return seed_points


def get_neighbors(x, y, direction="right"):
    """获取指定方向的邻域点（返回(x, y)格式）"""
    if direction == "right":
        return [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]  # 1, 0, 7方向
    else:
        # 其他方向可根据需要扩展
        return []


def track_line(image, start_point, end_x):
    """从种子点开始向右跟踪线路（使用(x, y)坐标系）"""
    height, width = image.shape
    x, y = start_point
    line_points = [(x, y)]

    while x < end_x:
        neighbors = get_neighbors(x, y, "right")
        valid_neighbors = []

        # 筛选有效邻域点
        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height:
                # 只考虑边缘点（二值化后为白色）
                if image[ny, nx] > 0:
                    valid_neighbors.append((nx, ny))

        if not valid_neighbors:
            break  # 无有效点，终止跟踪

        # 选择与当前方向最接近的点（简化版：优先水平方向）
        next_point = min(valid_neighbors, key=lambda p: abs(p[1] - y))

        # 更新当前点
        x, y = next_point
        line_points.append(next_point)

    return line_points


def extract_transmission_line(image, left_endpoints, right_end_x):
    """提取输电线边界线（使用(x, y)坐标系）"""
    boundary_lines = []
    for endpoint in left_endpoints:
        line = track_line(image, endpoint, right_end_x)
        boundary_lines.append(line)
    return boundary_lines


def process_lines(boundary_lines):
    """处理边界线生成输电线特征点"""
    if len(boundary_lines) < 2:
        return []

    top_line, bottom_line = boundary_lines[:2]
    feature_points = []

    # 生成特征点（取两条边界线的中心）
    for i in range(min(len(top_line), len(bottom_line))):
        x_top, y_top = top_line[i]
        x_bottom, y_bottom = bottom_line[i]

        # 计算中心点
        x_center = (x_top + x_bottom) // 2
        y_center = (y_top + y_bottom) // 2
        feature_points.append((x_center, y_center))

    return feature_points


# 示例使用
if __name__ == "__main__":
    # 读取图像
    image_gray = cv2.imread('../output/rectified_left1_image.png', cv2.IMREAD_GRAYSCALE)

    # # 二值化处理（假设输电线为白色）
    # _, binary_image = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)
    binary_image = image_gray.copy()

    # 转换为彩色图像用于标注
    image_color = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

    # 获取种子点
    seed_points = find_seed_points(binary_image)
    print(f"找到种子点数量: {len(seed_points)}")

    # 手动选择左端点（实际应用应自动检测）
    left_endpoints = []
    for x, y in seed_points:
        print("种子",x,y)
        if x < 50:  # 假设左端点在图像左侧
            left_endpoints.append((x, y))
            cv2.circle(image_color, (x, y), 5, (0, 255, 0), -1)  # 绿色标记种子点


    # 设置右边界（图像宽度-10）
    right_end_x = binary_image.shape[1] - 10

    # 提取边界线
    boundary_lines = extract_transmission_line(binary_image, left_endpoints, right_end_x)

    # 绘制边界线
    colors = [(255, 0, 0), (0, 0, 255)]  # 蓝、红
    for i, line in enumerate(boundary_lines):
        for x, y in line:
            cv2.circle(image_color, (x, y), 2, colors[i % 2], -1)

    # 生成特征点
    feature_points = process_lines(boundary_lines)

    # 绘制特征点
    for x, y in feature_points:
        cv2.circle(image_color, (x, y), 3, (0, 0, 255), -1)  # 红色特征点
        print("特征点")

    # 显示结果
    cv2.imshow('Result', image_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存结果
    cv2.imwrite('../output/line_points_marked.png', image_color)
    print("结果已保存")