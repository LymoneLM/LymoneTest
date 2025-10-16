import numpy as np
from PIL import Image, ImageDraw
import os

def create_loading_animation(output_path="loading.gif", size=100, frames=20, duration=100):
    """
    创建一个简单的加载动画GIF
    
    参数:
        output_path: 输出文件路径
        size: 图像大小 (像素)
        frames: 动画帧数
        duration: 每帧持续时间 (毫秒)
    """
    images = []
    center = size // 2
    max_radius = size // 2 - 5
    dot_radius = size // 10
    
    # 创建每一帧
    for i in range(frames):
        # 创建透明背景
        image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # 计算当前角度
        angle = 2 * np.pi * i / frames
        
        # 绘制加载圆点
        for j in range(8):  # 8个点
            # 计算点的角度
            a = angle + j * np.pi / 4
            
            # 计算点的位置
            x = center + int(max_radius * np.cos(a))
            y = center + int(max_radius * np.sin(a))
            
            # 计算点的大小和透明度 (基于与当前角度的距离)
            distance = (j * np.pi / 4 - angle) % (2 * np.pi)
            if distance > np.pi:
                distance = 2 * np.pi - distance
                
            alpha = int(255 * (1 - distance / np.pi))
            size_factor = 0.5 + 0.5 * (1 - distance / np.pi)
            r = int(dot_radius * size_factor)
            
            # 绘制点
            color = (41, 128, 185, alpha)  # 蓝色点，带透明度
            draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
        
        # 转换为RGB模式用于GIF
        rgb_image = Image.new('RGB', (size, size), (255, 255, 255))
        rgb_image.paste(image, (0, 0), image)
        images.append(rgb_image)
    
    # 保存GIF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        optimize=False
    )
    
    print(f"加载动画已保存至 {output_path}")

if __name__ == "__main__":
    create_loading_animation() 