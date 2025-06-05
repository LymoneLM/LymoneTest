import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io


def generate_line_plot():
    # 直线起点坐标
    x0, y0, z0 = 0, 0, 10000

    # 直线长度为 200m，即 200000mm
    length = 200000

    # 生成 x 坐标的值
    x = np.linspace(0, length, 100)

    # 利用二次函数模拟 y 轴负方向的轻微弯曲
    b = -0.0000006
    y = b * (x - length / 2) ** 2 + y0

    # 利用二次函数模拟 z 轴负方向的轻微弯曲
    a = 0.000001
    z = a * (x - length / 2) ** 2 + z0

    # 创建三维图形
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制曲线
    ax.plot(x, y, z, color='k', linestyle='-')

    # 设置坐标轴标签
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('A 200m line slightly curved in the negative y and z - directions')

    # 设置等比例坐标轴
    max_range = np.array([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()]).max()
    mid_x = (x.max() + x.min()) * 0.5
    mid_y = (y.max() + y.min()) * 0.5
    mid_z = (z.max() + z.min()) * 0.5
    ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
    ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)
    ax.set_zlim(mid_z - max_range / 2, mid_z + max_range / 2)

    # 生成 200 个随机点
    num_points = 200
    random_indices = np.random.choice(len(x), num_points)
    random_x = x[random_indices] + np.random.normal(0, 2000, num_points)
    random_y = y[random_indices] + np.random.normal(0, 2000, num_points)
    random_z = z[random_indices] + np.random.normal(0, 2000, num_points)

    # 绘制随机点
    ax.scatter(random_x, random_y, random_z, color='r', s=10, alpha=0.4)

    # 将图像保存为PNG格式的字节流
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close(fig)  # 关闭图形释放内存

    # 将图像转换为OpenCV格式 (NumPy数组)
    pil_image = Image.open(buf)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return opencv_image


# 使用示例
if __name__ == "__main__":
    # 获取OpenCV格式的图像
    cv_image = generate_line_plot()

    # 显示图像
    cv2.imshow('3D Line Plot', cv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存图像
    cv2.imwrite('./output/3d_line_plot.png', cv_image)
