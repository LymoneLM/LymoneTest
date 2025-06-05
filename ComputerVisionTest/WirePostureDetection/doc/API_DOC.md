# 项目API文档

> 自动生成的函数/方法文档

## 🗂️ 文件: `main.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `ImageProcessingApp.__init__` | `self` | 16 | No docstring |
| `ImageProcessingApp.initUI` | `self` | 33 | No docstring |
| `ImageProcessingApp.transfer_result_to_input` | `self` | 202 | No docstring |
| `ImageProcessingApp.import_stereo_images` | `self` | 221 | No docstring |
| `ImageProcessingApp.process_image` | `self, function_name` | 246 | No docstring |
| `ImageProcessingApp.display_image` | `self, image, label` | 303 | 在QLabel上显示OpenCV图像 |
| `ImageProcessingApp.resizeEvent` | `self, event` | 327 | 窗口大小改变时更新图像显示 |
| `__init__` | `self` | 16 | No docstring |
| `initUI` | `self` | 33 | No docstring |
| `transfer_result_to_input` | `self` | 202 | No docstring |
| `import_stereo_images` | `self` | 221 | No docstring |
| `process_image` | `self, function_name` | 246 | No docstring |
| `display_image` | `self, image, label` | 303 | 在QLabel上显示OpenCV图像 |
| `resizeEvent` | `self, event` | 327 | 窗口大小改变时更新图像显示 |


## 🗂️ 文件: `doc\makedoc.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `extract_methods` | `file_path` | 7 | 提取单个文件中的函数和方法 |
| `generate_docs` | `project_path, output_file` | 57 | 生成项目文档 |


## 🗂️ 文件: `src\bilateral_filter_enhancement.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `bilateral_filter_enhancement` | `input_image_path, output_image_path, d, sigma_color, sigma_space` | 5 | 双边滤波图像增强函数

参数:
    input_image_path (str): 输入图像路径
    output_image_path (str): 输出图像路径
    d (int): 领域直径，值越大处理范围越大，默认9
    sigma_color (int): 颜色空间滤波器的sigma值，值越大颜色相近的区域越容易被融合
    sigma_space (int): 坐标空间中滤波器的sigma值，值越大远处的像素越容易相互影响

返回:
    numpy.ndarray: 处理后的图像数组 |


## 🗂️ 文件: `src\bouguet_stereo_rectification.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `apply_stereo_rectification` | `img_left, img_right, R1, P1, R2, P2, camera_matrix_left, dist_coeffs_left, camera_matrix_right, dist_coeffs_right, image_size` | 6 | 应用双目校正结果到左右图像

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
rectified_img_right (numpy.ndarray): 右目校正后的图像 |
| `get_stereo_rectification` | `left_image, right_image` | 42 | No docstring |


## 🗂️ 文件: `src\canny.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `canny_edge_detection` | `image_path, low_threshold, high_threshold` | 6 | 使用Canny算子进行边缘检测

参数:
image_path (str): 图像文件的路径
low_threshold (int): Canny算子的低阈值
high_threshold (int): Canny算子的高阈值

返回:
edges (numpy.ndarray): 边缘检测后的图像 |
| `get_canny_edge_detection` | `input_img, low_threshold, high_threshold` | 29 | No docstring |


## 🗂️ 文件: `src\guided_filter_enhancement.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `guided_filter_enhancement` | `input_image_path, output_image_path, radius, eps` | 3 | 引导滤波图像增强函数

参数:
    input_image_path (str): 输入图像路径
    output_image_path (str): 输出图像路径
    radius (int): 引导滤波的半径，控制滤波的范围
    eps (float): 正则化参数，避免分母为零

返回:
    numpy.ndarray: 处理后的图像数组 |
| `get_guided_filter_enhancement` | `input_img, radius, eps` | 44 | No docstring |


## 🗂️ 文件: `src\image_grayscale_inversion.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `invert_grayscale_opencv` | `input_path, output_path` | 3 | No docstring |
| `get_invert_grayscale` | `input_img` | 15 | No docstring |


## 🗂️ 文件: `src\image_opening_operation.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `opening_operation` | `input_path, output_path` | 5 | No docstring |


## 🗂️ 文件: `src\krnel.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `convolve_image` | `image, kernel` | 10 | 对图像进行卷积操作
:param image: 输入图像
:param kernel: 卷积核
:return: 卷积后的图像 |
| `find_seed_points` | `image` | 30 | 找到种子点
:param image: 输入图像
:return: 种子点坐标列表 |
| `is_valid_point` | `x, y, height, width` | 44 | 检查点是否在图像范围内
:param x: 点的 x 坐标
:param y: 点的 y 坐标
:param height: 图像高度
:param width: 图像宽度
:return: 是否有效 |
| `get_neighbors` | `x, y` | 56 | 获取像素点右侧 1、0、7 方向的邻域点
:param x: 点的 x 坐标
:param y: 点的 y 坐标
:return: 邻域点列表 |
| `track_line` | `image, start_point, end_x` | 67 | 从种子点开始跟踪线路
:param image: 输入图像
:param start_point: 种子点坐标
:param end_x: 输电线右端点横坐标
:return: 跟踪到的线路坐标列表 |
| `extract_transmission_line` | `image, left_endpoints, right_end_x` | 94 | 提取输电线边界线的坐标
:param image: 输入图像
:param left_endpoints: 输电线边界线的左端点坐标列表
:param right_end_x: 输电线右端点横坐标
:return: 输电线边界线的坐标列表 |


## 🗂️ 文件: `src\pointpoint.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `generate_line_plot` | `` | 9 | No docstring |


## 🗂️ 文件: `src\PSNR.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `calculate_psnr` | `img1, img2` | 5 | 计算两张图片的峰值信噪比

参数:
    img1 (numpy.ndarray): 第一张图片
    img2 (numpy.ndarray): 第二张图片

返回:
    float: 峰值信噪比 |
| `main` | `` | 23 | No docstring |


## 🗂️ 文件: `src\resize.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `crop_images_in_boxes` | `image_path, output_paths, box_coordinates` | 3 | 在图片中截取每个指定正方形内的区域。

:param image_path: 图片路径
:param output_paths: 输出路径列表
:param box_coordinates: 每个正方形的坐标 (x_start, y_start, x_end, y_end) |


## 🗂️ 文件: `src\sobel.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `sobel_edge_detection` | `image_path, threshold` | 6 | 使用Sobel算子进行边缘检测

参数:
image_path (str): 图像文件的路径
threshold (int): 用于二值化的阈值

返回:
edges (numpy.ndarray): 边缘检测后的图像 |


## 🗂️ 文件: `src\xinxishang.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `calculate_psnr` | `img1, img2` | 5 | 计算两张图片的峰值信噪比

参数:
    img1 (numpy.ndarray): 第一张图片
    img2 (numpy.ndarray): 第二张图片

返回:
    float: 峰值信噪比 |
| `calculate_entropy` | `img` | 23 | 计算图像的信息熵

参数:
    img (numpy.ndarray): 输入图像

返回:
    float: 信息熵 |
| `calculate_weighted_psnr` | `img1, img2, weights` | 40 | 计算加权峰值信噪比

参数:
    img1 (numpy.ndarray): 第一张图片
    img2 (numpy.ndarray): 第二张图片
    weights (numpy.ndarray): 权重矩阵

返回:
    float: 加权峰值信噪比 |
| `main` | `` | 59 | No docstring |


## 🗂️ 文件: `src\zuobiao.py`

| 方法 | 参数 | 行号 | 描述 |
|------|------|------|------|
| `show_mouse_coordinates` | `image_path` | 3 | No docstring |
| `mouse_callback` | `event, x, y, flags, param` | 14 | No docstring |



## 统计信息

- 扫描文件总数: 15
- 成功处理文件: 15
- 失败文件数: 0