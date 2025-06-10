import cv2
import numpy as np

# 只考虑右侧三个方向：右上、右、右下
NEIGHBOR_OFFSETS = [(1, -1), (1, 0), (1, 1)]


def find_seed_points_from_binary_edge(edge_image, left_margin=50, max_seeds=3):
    """
    在边缘图中直接找白色像素作为种子点，从左侧挑选几个
    """
    all_edge_points = np.argwhere(edge_image == 255)
    left_seeds = [tuple(pt) for pt in all_edge_points if pt[1] < left_margin]
    left_seeds_sorted = sorted(left_seeds, key=lambda pt: pt[0])  # 按y排序，避免太近
    return left_seeds_sorted[:max_seeds]


def track_from_seed(image, seed, end_x):
    """
    沿 1, 0, 7 方向跟踪线条直到右端或断裂
    """
    h, w = image.shape
    path = [seed]
    visited = set()
    visited.add(seed)
    current = seed

    while current[1] < end_x:
        candidates = []
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = current[0] + dy, current[1] + dx
            if 0 <= nx < h and 0 <= ny < w and image[nx, ny] == 255:
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
        if len(path) > 1:
            all_paths.append(path)
    return all_paths


def extract_feature_points_from_paths(paths):
    """
    每条路径：按列（x坐标）分组，纵坐标取平均作为特征点
    """
    feature_points = []
    for path in paths:
        x_map = {}
        # for y, x in path:
        #     if x not in x_map:
        #         x_map[x] = []
        #     x_map[x].append(y)
        # for x, y_list in x_map.items():
        #     avg_y = int(np.mean(y_list))
        #     feature_points.append((avg_y, x))

        for x, y in path:
            if x not in x_map:
                x_map[x] = []
            x_map[x].append(y)
        for x, y_list in x_map.items():
            avg_y = int(np.mean(y_list))
            feature_points.append((avg_y, x))
    return feature_points


def draw_results(image, paths, feature_points, seeds):
    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 路径：蓝色
    for path in paths:
        for y, x in path:
            cv2.circle(output, (x, y), 1, (255, 0, 0), -1)

    # 特征点：红色
    for x, y in feature_points:
        cv2.circle(output, (x, y), 3, (0, 0, 255), -1)

    # 种子点：绿色
    for y, x in seeds:
        cv2.circle(output, (x, y), 3, (0, 255, 0), -1)

    return output

def do_kernal(image):

    # 1. 查找左边的种子点
    seeds = find_seed_points_from_binary_edge(image, left_margin=50, max_seeds=3)
    print("找到种子点数：", len(seeds))

    # 2. 跟踪路径
    rightmost_x = image.shape[1] - 1
    paths = extract_power_line_paths(image, seeds, rightmost_x)
    print("找到路径数：", len(paths))

    # 3. 提取特征点
    feature_points = extract_feature_points_from_paths(paths)
    print("提取特征点数：", len(feature_points))

    # 4. 绘制所有结果
    result_image = draw_results(image, paths, feature_points, seeds)

    # 5. 显示 + 保存
    cv2.imshow("Final Result", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("../output/powerline_features_result.png", result_image)
    print("结果已保存为 powerline_features_result.png")

    return np.array(feature_points)


if __name__ == "__main__":
    # 加载你的边缘图像
    image_left = cv2.imread("../output/ui_output_left.png", cv2.IMREAD_GRAYSCALE)
    image_right = cv2.imread("../output/ui_output_right.png", cv2.IMREAD_GRAYSCALE)

    # (y,x)格式
    np.save("../output/left_feature_points.npy", do_kernal(image_left))
    np.save("../output/right_feature_points.npy", do_kernal(image_right))
