import cv2

def crop_images_in_boxes(image_path, output_paths, box_coordinates):
    """
    在图片中截取每个指定正方形内的区域。

    :param image_path: 图片路径
    :param output_paths: 输出路径列表
    :param box_coordinates: 每个正方形的坐标 (x_start, y_start, x_end, y_end)
    """
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图片 {image_path}，请检查路径是否正确。")
        return

    # 对每个正方形进行操作
    for out_path, box in zip(output_paths, box_coordinates):
        x_start, y_start, x_end, y_end = box
        # 截取指定区域
        cropped_image = image[y_start:y_end, x_start:x_end]
        # 保存截取后的图片
        cv2.imwrite(out_path, cropped_image)
        print(f"已保存截取后的图片到 {out_path}")

# 示例使用
image_paths = ["output_gray.png", "output_opening.png", "output_image_filter.png", "output_image_guided.png"]  # 输入图片路径
output_paths = [
    ["cropped1_1.jpg", "cropped1_2.jpg", "cropped1_3.jpg"],  # image1 的输出路径
    ["cropped2_1.jpg", "cropped2_2.jpg", "cropped2_3.jpg"],  # image2 的输出路径
    ["cropped3_1.jpg", "cropped3_2.jpg", "cropped3_3.jpg"],  # image3 的输出路径
    ["cropped4_1.jpg", "cropped4_2.jpg", "cropped4_3.jpg"]   # image4 的输出路径
]
box_coordinates = [
    [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)],  # 第一张图片的正方形坐标
    [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)],  # 第二张图片的正方形坐标
    [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)],  # 第三张图片的正方形坐标
    [(25, 135, 85, 195), (270, 130, 330, 190), (570, 120, 630, 180)]   # 第四张图片的正方形坐标
]

# 遍历每张图片和对应的正方形坐标
for img_path, out_paths, boxes in zip(image_paths, output_paths, box_coordinates):
    crop_images_in_boxes(img_path, out_paths, boxes)