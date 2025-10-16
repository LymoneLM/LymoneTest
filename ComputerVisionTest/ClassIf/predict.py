import json
from PIL import Image
import torch
import torchvision.transforms as transforms
import os
import matplotlib.pyplot as plt
from moudle.mobilenet import MobileNetV2


def main():
    model_name = "mobilenet"

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    # 定义图像预处理
    data_transform = transforms.Compose([
                            transforms.Resize((224, 224)),
                            transforms.ToTensor(),
                            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    # 加载预测图像
    image_path = "datasets/val/swine_fever/swine_fever_0_SPN_18a66427.jpg"    # 图片输入路径
    assert os.path.exists(image_path), 'file:{} 不存在'.format(image_path)
    image = Image.open(image_path).convert('RGB')
    plt.imshow(image)
    image_tensor = data_transform(image).unsqueeze(0).to(device)

    # 读取类别
    json_path = "./class_indices.json"
    with open(json_path, 'r')as f:
        cls_dict = json.load(f)    # 加载类别标签
    # idx_class = {v: k for k, v in cls_dict.items()}

    # 创建模型

    if model_name == "mobilenet":
        # 定义模型MobileNetV2
        model = MobileNetV2(num_classes=2)
        weight_path = 'logs/' + model_name + "/best.pth"
        model.load_state_dict(torch.load(weight_path, map_location=device))

    model.to(device)   # 加载GPU或CPU

    # 开始预测
    model.eval()
    with torch.no_grad():
        output = torch.squeeze(model(image_tensor)).cpu()
        predict = torch.softmax(output, dim=0)  #
        predict_cls = torch.argmax(predict).numpy()  # 预测类别

    print_res = "label: {}     prob: {:.3}".format(cls_dict[str(predict_cls)],
                                                   predict[predict_cls].numpy())
    # 展示结果
    plt.title(print_res)
    plt.show()

if __name__ == '__main__':
    main()


