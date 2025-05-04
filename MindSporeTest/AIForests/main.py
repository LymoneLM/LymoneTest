# -*- coding: utf-8 -*-
from mindvision.dataset import ImageNet

# 数据集目录路径
data_path = "./images"

# 创建训练数据集
dataset_train = ImageNet(data_path, split="train", shuffle=True,
                         resize=224, batch_size=18, repeat_num=1)
dataset_train = dataset_train.run()

# 创建评估数据集
dataset_val = ImageNet(data_path, split="val", shuffle=True,
                       resize=224, batch_size=18, repeat_num=1)
dataset_val = dataset_val.run()

data = next(dataset_train.create_dict_iterator())
images = data["image"]
labels = data["label"]

print("Tensor of image", images.shape)
print("Labels:", labels)

import matplotlib.pyplot as plt
import numpy as np

# class_name对应label，按文件夹字符串从小到大的顺序标记label
class_name = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "8", 6: "11", 7: "12",
              8: "13", 9: "14", 10: "15"
    , 11: "16", 12: "17", 13: "18", 14: "19", 15: "21"}

plt.figure(figsize=(15, 7))
for i in range(len(labels)):
    # 获取图像及其对应的label
    data_image = images[i].asnumpy()
    data_label = labels[i]
    # 处理图像供展示使用
    data_image = np.transpose(data_image, (1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    data_image = std * data_image + mean
    data_image = np.clip(data_image, 0, 1)
    # 显示图像
    plt.subplot(3, 6, i + 1)
    plt.imshow(data_image)
    plt.title(class_name[int(labels[i].asnumpy())])
    plt.axis("off")

plt.show()

import mindspore.nn as nn
from mindvision.classification.models import resnet50
from mindspore import load_checkpoint, load_param_into_net
from mindspore.train import Model

net = resnet50(pretrained=True)


# 定义全连接层
class DenseHead(nn.Cell):
    def __init__(self, input_channel, num_classes):
        super(DenseHead, self).__init__()
        self.dense = nn.Dense(input_channel, num_classes)

    def construct(self, x):
        return self.dense(x)


# 全连接层输入层的大小
in_channels = net.head.dense.in_channels
# 输出通道数大小为狼狗分类数2
head = DenseHead(in_channels, 16)
# 重置全连接层
net.head = head

# 定义优化器和损失函数
opt = nn.Momentum(params=net.trainable_params(), learning_rate=0.001, momentum=0.9)
loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

# 实例化模型
model = Model(net, loss, opt, metrics={"Accuracy": nn.Accuracy()})

from mindvision.engine.callback import ValAccMonitor
from mindspore.train.callback import TimeMonitor

num_epochs = 16
model.train(num_epochs,
            dataset_train,
            callbacks=[ValAccMonitor(model, dataset_val, num_epochs), TimeMonitor()])

import matplotlib.pyplot as plt
from mindspore import Tensor


def visualize_model(best_ckpt_path, val_ds):
    num_class = 16  # 对狼和狗图像进行二分类
    net = resnet50(num_class)
    # 加载模型参数
    param_dict = load_checkpoint(best_ckpt_path)
    load_param_into_net(net, param_dict)
    model = Model(net)
    # 加载验证集的数据进行验证
    data = next(val_ds.create_dict_iterator())
    images = data["image"].asnumpy()
    labels = data["label"].asnumpy()
    class_name = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "8", 6: "11", 7: "12",
                  8: "13", 9: "14", 10: "15"
        , 11: "16", 12: "17", 13: "18", 14: "19", 15: "21"}
    # 预测图像类别
    output = model.predict(Tensor(data['image']))
    pred = np.argmax(output.asnumpy(), axis=1)

    # 显示图像及图像的预测值
    plt.figure(figsize=(15, 7))
    for i in range(len(labels)):
        plt.subplot(3, 6, i + 1)
        # 若预测正确，显示为蓝色；若预测错误，显示为红色
        color = 'blue' if pred[i] == labels[i] else 'red'
        plt.title('predict:{}'.format(class_name[pred[i]]), color=color)
        picture_show = np.transpose(images[i], (1, 2, 0))
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        picture_show = std * picture_show + mean
        picture_show = np.clip(picture_show, 0, 1)
        plt.imshow(picture_show)
        plt.axis('off')

    plt.show()


visualize_model('best.ckpt', dataset_val)


import mindspore.nn as nn
from mindvision.classification.models import resnet50
from mindspore import load_checkpoint, load_param_into_net
from mindspore.train import Model

net_work = resnet50(pretrained=True)

# 全连接层输入层的大小
in_channels = net_work.head.dense.in_channels
# 输出通道数大小为狼狗分类数2
head = DenseHead(in_channels, 16)
# 重置全连接层
net_work.head = head

# 冻结除最后一层外的所有参数
for param in net_work.get_parameters():
    if param.name not in ["head.dense.weight", "head.dense.bias"]:
        param.requires_grad = False

# 定义优化器和损失函数
opt = nn.Momentum(params=net_work.trainable_params(), learning_rate=0.001, momentum=0.5)
loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

# 实例化模型
model1 = Model(net_work, loss, opt, metrics={"Accuracy": nn.Accuracy()})

visualize_model('best.ckpt', dataset_val)
