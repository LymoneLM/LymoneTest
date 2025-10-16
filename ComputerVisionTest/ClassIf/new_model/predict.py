import json
import os
import numpy as np
import torch
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from new_model.model import ResNet18


def predict_single_image(image_path, model_path, class_indices_path):
    """
    使用ResNet18模型预测单张图像
    
    参数:
        image_path: 图像路径
        model_path: 模型权重路径
        class_indices_path: 类别索引文件路径
    
    返回:
        预测类别和置信度
    """
    # 检查文件是否存在
    assert os.path.exists(image_path), f"图像文件 {image_path} 不存在"
    assert os.path.exists(model_path), f"模型文件 {model_path} 不存在"
    assert os.path.exists(class_indices_path), f"类别索引文件 {class_indices_path} 不存在"
    
    # 加载类别信息
    with open(class_indices_path, 'r') as f:
        class_dict = json.load(f)
    
    # 设置设备
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")
    
    # 定义图像预处理
    data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 加载和预处理图像
    image = Image.open(image_path).convert('RGB')
    image_tensor = data_transform(image).unsqueeze(0).to(device)
    
    # 创建模型并加载权重
    model = ResNet18(num_classes=len(class_dict))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    # 执行预测
    with torch.no_grad():
        output = torch.squeeze(model(image_tensor)).cpu()
        predict = torch.softmax(output, dim=0)
        predict_class = torch.argmax(predict).numpy()
    
    # 获取预测类别和置信度
    class_name = class_dict[str(predict_class)]
    confidence = predict[predict_class].item()
    
    return class_name, confidence, image


def main():
    # 设置路径
    image_path = "datasets/val/swine_fever/swine_fever_0_SPN_18a66427.jpg"  # 示例图像路径
    
    # 查找最新的模型目录
    logs_dir = "./logs"
    resnet_dirs = [d for d in os.listdir(logs_dir) if d.startswith("resnet18_")]
    if not resnet_dirs:
        print("未找到ResNet18模型目录，请先训练模型")
        return
    
    # 按照时间戳排序，获取最新的模型目录
    latest_model_dir = sorted(resnet_dirs)[-1]
    model_path = os.path.join(logs_dir, latest_model_dir, "best.pth")
    class_indices_path = "new_model/class_indices.json"
    
    # 进行预测
    class_name, confidence, image = predict_single_image(image_path, model_path, class_indices_path)
    
    # 显示结果
    result_text = f"预测类别: {class_name}\n置信度: {confidence:.4f}"
    print(result_text)
    
    # 可视化结果
    plt.figure(figsize=(8, 6))
    plt.imshow(image)
    plt.title(result_text)
    plt.axis('off')
    plt.show()
    
    # 批量预测示例
    print("\n批量预测示例:")
    val_dir = "datasets/val"
    for class_folder in os.listdir(val_dir):
        class_path = os.path.join(val_dir, class_folder)
        if os.path.isdir(class_path):
            # 从每个类别中随机选择一张图像进行预测
            image_files = [f for f in os.listdir(class_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                sample_image = os.path.join(class_path, np.random.choice(image_files))
                class_name, confidence, _ = predict_single_image(sample_image, model_path, class_indices_path)
                print(f"真实类别: {class_folder}, 预测类别: {class_name}, 置信度: {confidence:.4f}, 图像: {sample_image}")


if __name__ == "__main__":
    main() 