import cv2

def show_mouse_coordinates(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图片 {image_path}，请检查路径是否正确。")
        return

    # 创建一个窗口
    cv2.namedWindow("Image")

    # 鼠标回调函数
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            # 获取鼠标指针下的像素值
            pixel_value = image[y, x]
            # 显示坐标和像素值
            print(f"鼠标位置: ({x}, {y}), 像素值: {pixel_value}")

    # 设置鼠标回调函数
    cv2.setMouseCallback("Image", mouse_callback)

    # 显示图片
    cv2.imshow("Image", image)

    # 等待按键事件
    cv2.waitKey(0)
    # 关闭所有窗口
    cv2.destroyAllWindows()

# 示例使用
image_path = "../output/output_gray.png"  # 输入图片路径
show_mouse_coordinates(image_path)