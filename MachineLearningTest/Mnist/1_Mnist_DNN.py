import numpy as np
import pandas as pd # 数据处理
import matplotlib.pyplot as plt # 画图
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

# Import Torch
import torch
import torch.nn as nn
from torch import nn, optim

import Model

import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='Mnist_DNN')

# 添加参数
parser.add_argument("-b", '--batch-size', type=int, help='Set batch size')
parser.add_argument("-l", '--learning-rate', type=float, help='Set learning rate')
parser.add_argument("-e", '--epochs', type=int, help='Set epochs')
parser.add_argument("-n", '--no', type=int, help='figure name number')

# 解析参数
args = parser.parse_args()

train = pd.read_csv("./data/MNIST_train.csv")
test = pd.read_csv("./data/MNIST_test.csv")
print("数据集样例：")
print(train.head())
y = train.label.values
X = train.drop("label",axis=1).values

#2D图像，像素值[0,255]  --> [0,1]  --> [-1, 1](神经网络的输入在-1到1之间更容易收敛)
X = X/255.0
X = (X)*2 - 1
#X = X.reshape(-1, 1, 28, 28)  #(samples, channels, height, width))
#%%
#验证集：20%
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.2)
#train set
X_train_tensor = torch.from_numpy(X_train).type(torch.float)
y_train_tensor = torch.from_numpy(y_train).type(torch.LongTensor) # data type is long

#test set
X_test_tensor = torch.from_numpy(X_test).type(torch.float)
y_test_tensor = torch.from_numpy(y_test).type(torch.LongTensor) # data type is long
# Set batch size
batch_size = 128
if args.batch_size is not None:
    batch_size = args.batch_size
print("Batch size:", batch_size)

# Pytorch train and test sets
train = torch.utils.data.TensorDataset(X_train_tensor,y_train_tensor)
test = torch.utils.data.TensorDataset(X_test_tensor,y_test_tensor)

# data loader
train_loader = torch.utils.data.DataLoader(train, batch_size = batch_size, shuffle = True)
test_loader = torch.utils.data.DataLoader(test, batch_size = batch_size, shuffle = True)
# 生成模型实例
model = Model.DNN()

# 损失函数
criterion = nn.CrossEntropyLoss(reduction='sum')

# 学习率超参
learning_rate = 0.01
if args.learning_rate is not None:
    learning_rate = args.learning_rate
print("learning rate:", learning_rate)

# 优化器
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
# optimizer = optim.SGD(model.parameters(), lr=learning_rate)

epochs = 15
if args.epochs is not None:
    epochs = args.epochs
print("epochs:", epochs)

train_losses, test_losses = [], []
n_train_samples = len(X_train_tensor)
n_test_samples = len(X_test_tensor)
for epoch in range(epochs):
    running_loss, running_acc = 0., 0.
    for (img, label) in train_loader:
        optimizer.zero_grad()
        output = model(img)
        loss = criterion(output, label)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predict = torch.max(output, 1)
        correct_num = (predict == label).sum()
        running_acc += correct_num.item()

    running_loss /= n_train_samples
    running_acc /= n_train_samples

    # 验证误差
    # Turn off gradients for validation
    with torch.no_grad():
        test_loss, test_acc = 0., 0.
        for images, labels in test_loader:
            output = model(images)
            loss = criterion(output, labels)

            test_loss += loss.item()
            _, predict = torch.max(output, 1)
            correct_num = (predict == labels).sum()
            test_acc += correct_num.item()

    test_loss /= n_test_samples
    test_acc /= n_test_samples

    train_losses.append(running_loss)
    test_losses.append(test_loss)

    print("Epoch: {}/{}.. ".format(epoch + 1, epochs),
          "Training Loss: {:.3f}.. ".format(train_losses[-1]),
          "Training Accuracy: {:.3f} %".format(100 * running_acc),
          "Test Loss: {:.3f}.. ".format(test_losses[-1]),
          "Test Accuracy: {:.3f} %".format(100 * test_acc))

# 保存模型
torch.save(model, 'fc.pth.tar')

# Test the model
model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Test Accuracy of the model on the 10000 test images: {} %'.format(100 * correct / total))

# Save the model checkpoint
output_path = "./output"
no = 0
if args.no is not None:
    no = args.no
torch.save(model.state_dict(), f'{output_path}/model_{no}.ckpt')
plt.plot(train_losses, label='Training loss')
plt.plot(test_losses, label='Validation loss')

plt.xlabel("epochs")
plt.ylabel("loss")

plt.legend(frameon=False)
plt.savefig(f'{output_path}/loss_{no}.png')
# plt.show()