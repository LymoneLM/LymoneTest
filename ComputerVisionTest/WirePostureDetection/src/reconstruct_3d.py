import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv


def load_feature_points(path):
    """
    加载特征点坐标文件，格式为 [(y, x), ...]
    """
    return np.load(path, allow_pickle=True)


def match_feature_points(left_pts, right_pts, x0_thresh=100, max_disparity=100, y_tolerance=3):
    """
    论文方法改进版：y 值允许在 ±y_tolerance 范围内波动
    """
    from collections import defaultdict

    matches = []
    # 构建右图字典：y → list of x
    right_dict = defaultdict(list)
    for x, y in right_pts:
        right_dict[y].append(x)

    for xL, yL in left_pts:
        matched = False
        for dy in range(-y_tolerance, y_tolerance + 1):
            yR = yL + dy
            if yR not in right_dict:
                continue
            xR_candidates = right_dict[yR]

            if xL > x0_thresh:
                valid = [xR for xR in xR_candidates if xR < x0_thresh and 0 < xL - xR < max_disparity]
            else:
                valid = [xR for xR in xR_candidates if xR > x0_thresh and 0 < xR - xL < max_disparity]

            if valid:
                # 选择最接近的
                xR_best = min(valid, key=lambda xR: abs(xL - xR))
                matches.append(((xL, yL), (xR_best, yR)))
                matched = True
                break  # 找到就不再尝试其它y

    return matches


def compute_3d_coords(matches, f, b):
    """
    根据视差公式计算三维坐标
    Z = f*b / d, X = Z*x/f, Y = Z*y/f
    """
    points_3d = []
    for (xL, y), (xR, _) in matches:
        d = xL - xR
        if d == 0:
            continue
        Z = f * b / d
        X = Z * xL / f
        Y = Z * y / f
        points_3d.append((X, Y, Z))
    return np.array(points_3d)


def visualize_3d(points_3d):
    """
    使用matplotlib可视化三维点云
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points_3d[:, 0], points_3d[:, 1], points_3d[:, 2], c='r', s=10)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title("3D Point Cloud")
    plt.tight_layout()
    plt.show()


def save_to_csv(points, path="3d_points.csv"):
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["X", "Y", "Z"])
        for pt in points:
            writer.writerow(pt)


if __name__ == "__main__":
    # 加载左右图的特征点（需先存为.npy或.txt）
    left_points = load_feature_points("../output/left_feature_points.npy")
    right_points = load_feature_points("../output/right_feature_points.npy")

    # 相机参数（单位：mm）
    f = 384.24
    b = 50.1

    # 匹配点对
    matches = match_feature_points(left_points, right_points)
    print(matches)
    print("成功匹配点对数量：", len(matches))

    # 计算三维坐标
    points_3d = compute_3d_coords(matches, f, b)
    print("<UNK>", len(points_3d))

    # 可视化和保存
    visualize_3d(points_3d)
    save_to_csv(points_3d)
    print("3D坐标保存完毕：3d_points.csv")
