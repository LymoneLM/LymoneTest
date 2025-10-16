import os
import random
import cv2
import numpy as np


class RandomImageEnhancer:
    def __init__(self, root_path):
        self.root_path = root_path
        self.export_base = root_path.rsplit('.', 1)[0]
        self.class_name = os.path.basename(os.path.dirname(root_path))
        self.image = cv2.imread(root_path)
        if self.image is None:
            raise ValueError(f"图像加载失败: {root_path}")

    def _random_param(self, low, high, decimal=False):
        """生成随机参数"""
        if decimal:
            return round(random.uniform(low, high), 2)
        return random.randint(int(low), int(high))

    def _save(self, img, operation):
        """保存增强结果"""
        save_path = f'{self.export_base}_{operation}_{random.getrandbits(32):08x}.jpg'
        cv2.imwrite(save_path, img)

    def salt_pepper_noise(self):
        """随机椒盐噪声 (概率范围: 0.5%-5%)"""
        prob = self._random_param(0.005, 0.05, decimal=True)
        noisy = self.image.copy()

        # 生成随机掩膜
        salt_mask = np.random.rand(*self.image.shape[:2]) < prob / 2
        pepper_mask = np.random.rand(*self.image.shape[:2]) < prob / 2

        noisy[salt_mask] = 255
        noisy[pepper_mask] = 0
        self._save(noisy, 'SPN')
        return self

    def gaussian_noise(self):
        """随机高斯噪声 (标准差范围: 10-50)"""
        sigma = self._random_param(10, 50)
        # 修复步骤：确保数据类型一致
        gauss = np.random.normal(0, sigma, self.image.shape).astype(np.float32)  # 添加类型转换
        noisy = cv2.add(self.image.astype(np.float32), gauss)  # 保证两个参数都是float32
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        self._save(noisy, 'GauN')
        return self

    def random_brightness(self):
        """随机亮度调整 (系数范围: 0.3-2.0)"""
        factor = self._random_param(0.3, 2.0, decimal=True)
        bright = cv2.convertScaleAbs(self.image, alpha=factor, beta=0)
        self._save(bright, 'Bright')
        return self

    def random_rotation(self):
        """随机旋转 (角度范围: -45°~45°, 缩放范围: 0.8-1.2)"""
        angle = self._random_param(-45, 45)
        scale = self._random_param(0.8, 1.2, decimal=True)

        h, w = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(self.image, M, (w, h))
        self._save(rotated, 'Rot')
        return self

    def random_flip(self):
        """随机翻转 (水平/垂直/双向)"""
        flip_code = random.choice([-1, 0, 1])
        flipped = cv2.flip(self.image, flip_code)
        self._save(flipped, f'Flip{flip_code}')
        return self

    def random_crop(self):
        """随机裁剪 (保留比例: 60%-95%)"""
        h, w = self.image.shape[:2]
        crop_ratio = self._random_param(0.6, 0.95, decimal=True)
        new_h, new_w = int(h * crop_ratio), int(w * crop_ratio)

        y = random.randint(0, h - new_h)
        x = random.randint(0, w - new_w)
        cropped = self.image[y:y + new_h, x:x + new_w]
        cropped = cv2.resize(cropped, (w, h))  # 保持原始尺寸
        self._save(cropped, 'Crop')
        return self

    def color_jitter(self):
        """随机颜色抖动 (HSV空间)"""
        # 转换到HSV空间
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV).astype(np.float32)

        # 随机参数范围
        h_shift = random.randint(-15, 15)  # 色相偏移
        s_scale = random.uniform(0.7, 1.3)  # 饱和度缩放
        v_scale = random.uniform(0.7, 1.3)  # 明度缩放

        # 应用变换
        hsv[..., 0] = (hsv[..., 0] + h_shift) % 180
        hsv[..., 1] = np.clip(hsv[..., 1] * s_scale, 0, 255)
        hsv[..., 2] = np.clip(hsv[..., 2] * v_scale, 0, 255)

        # 转换回BGR时确保类型正确
        jittered = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        self._save(jittered, 'Color')
        return self

    def random_blur(self):
        """随机模糊 (核大小: 1-7的奇数)"""
        ksize = random.choice([1, 3, 5, 7])
        blurred = cv2.GaussianBlur(self.image, (ksize, ksize), 0)
        self._save(blurred, 'Blur')
        return self


def process_directory(root_dir, augmentations_per_image=5):
    """
    处理目录中的所有图像
    :param root_dir: 根目录路径
    :param augmentations_per_image: 每张图片应用的增强次数
    """
    enhancers = [
        RandomImageEnhancer.salt_pepper_noise,
        RandomImageEnhancer.gaussian_noise,
        RandomImageEnhancer.random_brightness,
        RandomImageEnhancer.random_rotation,
        RandomImageEnhancer.random_flip,
        RandomImageEnhancer.random_crop,
        RandomImageEnhancer.color_jitter,
        RandomImageEnhancer.random_blur
    ]

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                try:
                    img_path = os.path.join(root, file)
                    enhancer = RandomImageEnhancer(img_path)

                    # 随机选择增强方法
                    selected = random.sample(enhancers, k=augmentations_per_image)
                    for method in selected:
                        method(enhancer)

                except Exception as e:
                    print(f"处理 {img_path} 时出错: {str(e)}")


if __name__ == '__main__':
    process_directory('../datasets/train/health', augmentations_per_image=1)