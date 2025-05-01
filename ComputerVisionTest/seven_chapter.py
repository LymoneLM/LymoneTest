import cv2
import numpy

def process_image(input_path, output_path):
    # 图像预处理流程
    image_data = cv2.imread(input_path)
    hsv_space = cv2.cvtColor(image_data, cv2.COLOR_BGR2HSV)
    hue_component = hsv_space[:, :, 0]

    # 数据预处理
    sample_points = hue_component.reshape(-1, 1).astype(numpy.float32)
    data_count = sample_points.shape[0]

    # 算法参数配置
    cluster_num = 3
    max_cycles = 100
    convergence_threshold = 1e-4
    numpy.random.seed(42)

    # 中心点初始化
    random_selection = numpy.random.choice(data_count, cluster_num, False)
    cluster_centers = sample_points[random_selection].flatten()

    # 迭代优化过程
    for iteration in range(max_cycles):
        # 计算样本距离
        delta = numpy.abs(sample_points - cluster_centers.reshape(1, -1))
        circular_dist = numpy.minimum(delta, 180 - delta)
        cluster_labels = numpy.argmin(circular_dist, axis=1)

        # 更新中心位置
        updated_centers = numpy.zeros_like(cluster_centers)
        for cluster_id in range(cluster_num):
            group_data = sample_points[cluster_labels == cluster_id]
            if group_data.size == 0:
                updated_centers[cluster_id] = cluster_centers[cluster_id]
                continue

            # 环形数据平均计算
            rad_values = numpy.deg2rad(group_data * 2)
            mean_vector = [
                numpy.mean(numpy.cos(rad_values)),
                numpy.mean(numpy.sin(rad_values))
            ]
            angle_rad = numpy.arctan2(*mean_vector[::-1])
            mean_hue = (numpy.rad2deg(angle_rad) / 2) % 180
            updated_centers[cluster_id] = mean_hue

        # 收敛性判断
        if numpy.allclose(cluster_centers, updated_centers,
                         atol=convergence_threshold):
            break
        cluster_centers = updated_centers.copy()

    # 结果重构与输出
    quantized_hue = numpy.round(cluster_centers[cluster_labels]
                              ).astype(numpy.uint8) % 180
    result_hsv = cv2.merge([
        quantized_hue.reshape(hue_component.shape),
        numpy.full_like(hue_component, 255),
        numpy.full_like(hue_component, 255)
    ])
    output_data = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2BGR)

    # 保存处理结果
    cv2.imwrite(output_path, output_data)
    cv2.imshow('Segmentation Result', output_data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image(r'.\img\fruit.jpg', 'fruit_kmeans_segmented.jpg')