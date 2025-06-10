# MNIST数据集准备
import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision import transforms
from torch import nn
from Model import CNN
import math
# batch_size超参，根据硬件配置相应大小
batch_size = ?

trans_img = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
    ])

# MNIST数据集每张图片是灰度图片，大小为28x28
trainset = MNIST('data', train=True, download=True, transform=trans_img)
testset = MNIST('data', train=False, download=True, transform=trans_img)
train_loader = DataLoader(trainset, batch_size=batch_size,
                          shuffle=True, num_workers=0)
test_loader = DataLoader(testset, batch_size=batch_size,
                          shuffle=True, num_workers=0)# 运行环境
import matplotlib.pyplot as plt

# plt.ion()
cnt = 0
for (img_batch, label) in train_loader:
    cnt += 1
    if cnt > 10:
        break
    fig, ax = plt.subplots(
        nrows=4,
        ncols=8,
        sharex=True,
        sharey=True, )
    ax = ax.flatten()
    for i in range(32):
        img = img_batch[i].numpy().reshape(28, 28)
        ax[i].imshow(img, cmap='Greys', interpolation='nearest')

    ax[0].set_xticks([])
    ax[0].set_yticks([])
#     plt.show()
#     plt.close()
# plt.ioff()
from torch import optim
from torch.autograd import Variable
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
# model = CNN().cuda()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = CNN().to(device)
learning_rate = ?
criterion = nn.CrossEntropyLoss(size_average=False)
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# 总的训练轮数
epochs = ?
train_losses = []
test_losses = []
for epoch in range(epochs):
    running_loss, running_acc = 0., 0.
    for (img, label) in train_loader:
        # img = Variable(img).cuda()
        img = Variable(img).to(device)
        # label = Variable(label).cuda()
        img = Variable(img).to(device)

        optimizer.zero_grad()
        output = model(img)
        loss = criterion(output, label)
        # print()

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predict = torch.max(output, 1)
        correct_num = (predict == label).sum()
        running_acc += correct_num.item()

    running_loss /= len(trainset)
    running_acc /= len(trainset)

    with torch.no_grad():
        test_loss, test_acc = 0., 0.
        for images, labels in test_loader:
            # images = Variable(images).cuda()
            images = Variable(images).to(device)
            # labels = Variable(labels).cuda()
            labels = Variable(labels).to(device)
            output = model(images)
            loss = criterion(output, labels)

            test_loss += loss.item()
            _, predict = torch.max(output, 1)
            correct_num = (predict == labels).sum()
            test_acc += correct_num.item()

    test_loss /= len(testset)
    test_acc /= len(testset)

    train_losses.append(running_loss)
    test_losses.append(test_loss)
    print("Epoch: {}/{}.. ".format(epoch + 1, epochs),
          "Training Loss: {:.3f}.. ".format(train_losses[-1]),
          "Training Accuracy: {:.3f} %".format(100 * running_acc),
          "Test Loss: {:.3f}.. ".format(test_losses[-1]),
          "Test Accuracy: {:.3f} %".format(100 * test_acc))
# 保存模型
torch.save(model, 'conv.pth.tar')
plt.plot(train_losses, label='Training loss')
plt.plot(test_losses, label='Validation loss')
plt.xlabel("epochs")
plt.ylabel("loss")
plt.legend(frameon=False)
plt.show()
model = torch.load('conv.pth.tar')
print('testing cnn model')
testloss, testacc = 0., 0.
for (img, label) in test_loader:
    # img = Variable(img).cuda()
    img = Variable(img).to(device)
    # label = Variable(label).cuda()
    label = Variable(label).to(device)
    out = model(img)
    loss = criterion(out, label)
    testloss += loss.item()
    _, predict = torch.max(out, 1)
    correct_num = (predict == label).sum()
    testacc += correct_num.item()

testloss /= len(testset)
testacc /= len(testset)
print('cnn model, Test: Loss: %.5f, Acc: %.2f' %
      (testloss, 100 * testacc))