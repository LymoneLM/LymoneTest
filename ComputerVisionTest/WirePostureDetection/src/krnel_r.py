import cv2
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)


# 三个用于提取边缘的核
KERNELS = [
    np.array([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]]),
    np.array([[-1, -1, 1], [-1, 1, -1], [1, -1, -1]]),
    np.array([[-1, -1, -1], [1, 1, 1], [-1, -1, -1]])
]

# 仅考虑右侧的三个方向 (1, 0, 7)
NEIGHBOR_OFFSETS = [(1, -1), (1, 0), (1, 1)]  # 右上、右、右下


def apply_kernels_and_find_seeds(image):
    response = sum([cv2.filter2D(image, -1, k) for k in KERNELS])
    seed_points = np.argwhere(response == 3)
    return [tuple(pt) for pt in seed_points]


def track_from_seed(image, seed, end_x):
    h, w = image.shape
    path = [seed]
    visited = set()
    visited.add(seed)
    current = seed

    while current[1] < end_x:
        candidates = []
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = current[0] + dy, current[1] + dx
            if 0 <= nx < h and 0 <= ny < w and image[nx, ny] > 0:
                if (nx, ny) not in visited:
                    candidates.append((nx, ny))
        if not candidates:
            break
        current = candidates[0]
        path.append(current)
        visited.add(current)

    return path


def extract_power_line_paths(image, left_seeds, end_x):
    all_paths = []
    for seed in left_seeds:
        path = track_from_seed(image, seed, end_x)
        all_paths.append(path)
    return all_paths


def extract_feature_points_from_paths(paths):
    """
    每条路径中取一定间隔的点为特征点，或者取平均坐标值
    """
    feature_points = []
    for path in paths:
        if not path:
            continue
        # 以横坐标分组，每列保留一个纵坐标点（取平均）
        x_map = {}
        for y, x in path:
            if x not in x_map:
                x_map[x] = []
            x_map[x].append(y)
        for x, y_list in x_map.items():
            avg_y = int(np.mean(y_list))
            feature_points.append((avg_y, x))
    return feature_points


def draw_results(image, paths, feature_points):
    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for path in paths:
        for y, x in path:
            cv2.circle(output, (x, y), 1, (255, 0, 0), -1)  # 蓝色路径点
    for y, x in feature_points:
        cv2.circle(output, (x, y), 3, (0, 0, 255), -1)  # 红色特征点
    return output


if __name__ == "__main__":
    image = cv2.imread("../output/ui_output_left.png", cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("图像加载失败，请检查路径")

    # 自动提取种子点
    seeds = apply_kernels_and_find_seeds(image)
    logging.info("{} seeds found".format(len(seeds)))

    # 手动选前2个左侧种子点（模拟左端点）
    left_seeds = [pt for pt in seeds if pt[1] < 50][:2]
    rightmost_x = image.shape[1] - 1

    # 跟踪路径
    paths = extract_power_line_paths(image, left_seeds, rightmost_x)
    logging.info("{} paths found".format(len(paths)))

    # 提取特征点
    feature_points = extract_feature_points_from_paths(paths)
    logging.info("{} feature_points found".format(len(feature_points)))

    # 可视化
    result_img = draw_results(image, paths, feature_points)

    # 显示
    cv2.imshow("Powerline with Features", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存
    cv2.imwrite("../output/powerline_feature_result.png", result_img)
    print("特征提取图像已保存: powerline_feature_result.png")
