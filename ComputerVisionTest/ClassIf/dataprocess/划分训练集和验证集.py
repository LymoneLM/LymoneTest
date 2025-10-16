import os
import shutil
import random
import cv2

train_root = "../datasets/train"
val_root = "../datasets/val"

name_list = os.listdir(train_root)
for name in name_list:
    image_root = os.path.join(train_root, name)
    image_list = os.listdir(image_root)

    # 随机打乱文件名列表
    random.shuffle(image_list)
    num_images = len(image_list)
    num_val = int(num_images * 0.2)
    val_names = image_list[:num_val]

    for image_name in val_names:
        image_path = os.path.join(image_root, image_name)
        print(image_path)
        save_root = os.path.join(val_root, name)
        if not os.path.exists(save_root):
            os.makedirs(save_root)
        save_image_path = os.path.join(save_root, image_name)
        print(save_image_path)
        if os.path.exists(save_image_path) is False:
            shutil.move(image_path, save_image_path)
