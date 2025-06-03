import cv2

def invert_grayscale_opencv(input_path, output_path):
    try:
        # 以灰度模式读取图像
        image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        # 灰度反转
        inverted_image = 255 - image
        # 保存图像
        cv2.imwrite(output_path, inverted_image)
        print(f"处理后的图像已保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def get_invert_grayscale(input_img):
    try:
        inverted_image = 255 - input_img
        return inverted_image
    except Exception as e:
        print(f"发生错误: {e}")
        return None


if __name__ == "__main__":
    input_image_path = '../output/right_image.png'
    output_image_path = '../output/right1_output_gray.png'
    invert_grayscale_opencv(input_image_path, output_image_path)