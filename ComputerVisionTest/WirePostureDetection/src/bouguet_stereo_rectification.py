import cv2
import numpy as np
from fontTools.ttx import process


def apply_stereo_rectification(img_left, img_right, R1, P1, R2, P2, camera_matrix_left, dist_coeffs_left,
                               camera_matrix_right, dist_coeffs_right, image_size):
    """
    应用双目校正结果到左右图像

    参数:
    img_left (numpy.ndarray): 左目原始图像
    img_right (numpy.ndarray): 右目原始图像
    R1 (numpy.ndarray): 左目旋转矩阵
    P1 (numpy.ndarray): 左目投影矩阵
    R2 (numpy.ndarray): 右目旋转矩阵
    P2 (numpy.ndarray): 右目投影矩阵
    camera_matrix_left (numpy.ndarray): 左目相机内参矩阵
    dist_coeffs_left (numpy.ndarray): 左目相机畸变系数
    camera_matrix_right (numpy.ndarray): 右目相机内参矩阵
    dist_coeffs_right (numpy.ndarray): 右目相机畸变系数
    image_size (tuple): 图像尺寸 (宽度, 高度)

    返回:
    rectified_img_left (numpy.ndarray): 左目校正后的图像
    rectified_img_right (numpy.ndarray): 右目校正后的图像
    """
    # 计算校正映射
    map1_left, map2_left = cv2.initUndistortRectifyMap(
        camera_matrix_left, dist_coeffs_left, R1, P1, image_size, cv2.CV_16SC2
    )
    map1_right, map2_right = cv2.initUndistortRectifyMap(
        camera_matrix_right, dist_coeffs_right, R2, P2, image_size, cv2.CV_16SC2
    )

    # 应用校正映射
    rectified_img_left = cv2.remap(img_left, map1_left, map2_left, cv2.INTER_LINEAR)
    rectified_img_right = cv2.remap(img_right, map1_right, map2_right, cv2.INTER_LINEAR)

    return rectified_img_left, rectified_img_right

def get_stereo_rectification(left_image, right_image):
    # 已知的双目校正结果
    R1 = np.array([
        [9.98804227e-01, 4.09616624e-03, -4.87169052e-02],
        [-4.04315662e-03, 9.99991122e-01, 1.18660966e-03],
        [4.87213333e-02, -9.88220664e-04, 9.98811922e-01]
    ])
    P1 = np.array([
        [384.23980757, 0., 342.7240839, 0.],
        [0., 384.23980757, 238.35979748, 0.],
        [0., 0., 1., 0.]
    ])
    R2 = np.array([
        [9.98799478e-01, 3.91219577e-03, -4.88292729e-02],
        [-3.96532298e-03, 9.99991647e-01, -9.91196927e-04],
        [4.88249873e-02, 1.18363081e-03, 9.98806648e-01]
    ])
    P2 = np.array([
        [384.23980757, 0., 342.7240839, -19.24920764],
        [0., 384.23980757, 238.35979748, 0.],
        [0., 0., 1., 0.]
    ])

    # 相机内参矩阵和畸变系数
    camera_matrix_left = np.array([
        [382.35897727, 0., 316.98197539],
        [0., 384.07079069, 241.42621517],
        [0., 0., 1.]
    ])
    dist_coeffs_left = np.array([-0.00805413, -0.20524819, -0.00411927, -0.00268155, 0.85836507])
    camera_matrix_right = np.array([
        [382.70401174, 0., 317.28458035],
        [0., 384.40882445, 240.58905459],
        [0., 0., 1.]
    ])
    dist_coeffs_right = np.array([-0.00489881, -0.25870044, -0.00480808, -0.00284292, 1.20272261])

    if left_image is None or right_image is None:
        print("Error: Could not read one or both of the images.")
    else:
        image_size = (left_image.shape[1], left_image.shape[0])
        processed_left, processed_right = apply_stereo_rectification(
            left_image, right_image, R1, P1, R2, P2, camera_matrix_left, dist_coeffs_left,
            camera_matrix_right, dist_coeffs_right, image_size
        )

        def get_valid_mask(img):
            """创建有效像素的掩码，兼容单通道和三通道图像"""
            if len(img.shape) == 2:  # 单通道图像
                return (img > 0).astype(np.uint8) * 255
            else:  # 多通道图像
                # 计算每个像素是否在所有通道上都有有效值
                mask = np.all(img > 0, axis=2).astype(np.uint8) * 255
                return mask

        # 获取左右图的掩码
        mask_left = get_valid_mask(processed_left)
        mask_right = get_valid_mask(processed_right)

        # 计算共同有效区域
        combined_mask = cv2.bitwise_and(mask_left, mask_right)

        # 找到共同有效区域的外接矩形
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print("Warning: No valid region found. Returning uncropped images.")
            return processed_left, processed_right

        # 获取最大轮廓的外接矩形
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)

        # 添加安全边界（确保完全去除边缘）
        border = 1  # 1像素安全边界
        x = max(0, x + border)
        y = max(0, y + border)
        w = max(0, w - 2 * border)
        h = max(0, h - 2 * border)

        # 执行裁剪
        if w > 0 and h > 0:
            processed_left = processed_left[y:y + h, x:x + w]
            processed_right = processed_right[y:y + h, x:x + w]
        else:
            print("Warning: Crop region invalid. Returning uncropped images.")

        if len(processed_left.shape) == 2:
            processed_left = cv2.cvtColor(processed_left, cv2.COLOR_GRAY2BGR)
        if len(processed_right.shape) == 2:
            processed_right = cv2.cvtColor(processed_right, cv2.COLOR_GRAY2BGR)

        return processed_left, processed_right
    return None


if __name__ == "__main__":

    # 读取左右图像
    img_left = cv2.imread('../output/left1_output_image_guided.png')
    img_right = cv2.imread('../output/right1_output_image_guided.png')

    rectified_img_left, rectified_img_right = get_stereo_rectification(img_left, img_right)

    # 显示校正后的图像
    cv2.imshow('Rectified Left Image', rectified_img_left)
    cv2.imshow('Rectified Right Image', rectified_img_right)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存校正后的图像
    cv2.imwrite('../output/rectified_left1_image.png', rectified_img_left)
    cv2.imwrite('../output/rectified_right1_image.png', rectified_img_right)



