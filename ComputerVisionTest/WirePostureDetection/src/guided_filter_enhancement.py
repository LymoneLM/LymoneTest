import cv2

def guided_filter_enhancement(input_image_path, output_image_path, radius=5, eps=0.01):
    """
    引导滤波图像增强函数

    参数:
        input_image_path (str): 输入图像路径
        output_image_path (str): 输出图像路径
        radius (int): 引导滤波的半径，控制滤波的范围
        eps (float): 正则化参数，避免分母为零

    返回:
        numpy.ndarray: 处理后的图像数组
    """
    try:
        # 读取图像（支持彩色和灰度图像）
        image = cv2.imread(input_image_path)

        if image is None:
            raise ValueError("无法读取输入图像，请检查文件路径和图像格式")

        # 转换为灰度图像（如果是彩色图像）
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        # 应用引导滤波
        enhanced_image = cv2.ximgproc.guidedFilter(gray_image, gray_image, radius, eps)

        # 自动对比度增强
        enhanced_image = cv2.equalizeHist(enhanced_image)

        # 保存处理后的图像
        cv2.imwrite(output_image_path, enhanced_image)

        return enhanced_image

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None

def get_guided_filter_enhancement(input_img, radius = 5, eps = 0.01):
    try:
        if len(input_img.shape) == 3:
            gray_image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = input_img

        # 应用引导滤波
        enhanced_image = cv2.ximgproc.guidedFilter(gray_image, gray_image, radius, eps)

        # 自动对比度增强（可选步骤，提升视觉效果）
        enhanced_image = cv2.equalizeHist(enhanced_image)

        return enhanced_image

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None


if __name__ == "__main__":
    # 配置参数
    INPUT_IMAGE_PATH = "../output/right1_output_gray.png"  # 输入图像路径
    OUTPUT_IMAGE_PATH = "../output/right1_output_image_guided.png"  # 输出图像路径

    # 执行引导滤波增强
    processed_image = guided_filter_enhancement(
        INPUT_IMAGE_PATH,
        OUTPUT_IMAGE_PATH,
        radius=5,
        eps=0.01
    )

    if processed_image is not None:
        print("图像增强处理完成并已保存")

        # 可选：在图形界面中显示结果（需安装GUI环境）
        if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) >= 0:
            cv2.imshow("Original Image", cv2.imread(INPUT_IMAGE_PATH))
            cv2.imshow("Enhanced Image", processed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()