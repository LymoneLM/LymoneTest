import json
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
import itertools
from sklearn.metrics import confusion_matrix
import shutil
import glob
from datetime import datetime

import torch
from torch import nn
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

# 导入ResNet18模型
from new_model.model import ResNet18


def main():
    model_name = "resnet18"    # 使用ResNet18模型
    log_dir = "./logs"
    
    # 完全重建日志目录
    print("正在清理和重建日志目录...")
    
    # 使用时间戳创建唯一日志目录，避免冲突
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_root = os.path.join(log_dir, f"{model_name}_{timestamp}")
    
    # 确保新的日志目录存在
    os.makedirs(log_root, exist_ok=True)
    print(f"创建日志目录: {log_root}")
        
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    # 数据预处理   随机裁剪  镜像
    train_transform = torchvision.transforms.Compose([torchvision.transforms.RandomResizedCrop(224),
                                                     torchvision.transforms.RandomHorizontalFlip(),
                                                     torchvision.transforms.ToTensor(),
                                                     torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                                                                      [0.229, 0.224, 0.225])])


    test_transform = torchvision.transforms.Compose([torchvision.transforms.Resize(256),
                                                   torchvision.transforms.CenterCrop(224),
                                                   torchvision.transforms.ToTensor(),
                                                   torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                                                                    [0.229, 0.224, 0.225])])

    # 定义数据集
    dataest_path = "./datasets"
    assert os.path.exists(dataest_path), "{}路径不存在.".format(dataest_path)
    train_dataset = torchvision.datasets.ImageFolder(root=os.path.join(dataest_path, "train"),
                                                     transform=train_transform)
    val_dataset = torchvision.datasets.ImageFolder(root=os.path.join(dataest_path, "val"),
                                                     transform=test_transform)
    train_num = len(train_dataset)  # 获取训练集长度
    val_num = len(val_dataset)  # 获取验证集长度

    data_list = train_dataset.class_to_idx
    cls_dict = dict((val, key) for key, val in data_list.items())  # Python 字典(Dictionary) items() 函数以列表返回可遍历的(键, 值) 元组数组
    # write dict into json file
    json_str = json.dumps(cls_dict, indent=4)
    with open('new_model/class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    # 加载数据集
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)  # 调整批次大小为32
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=True)
    print("using {} images for training, {} images for validation.".format(train_num, val_num))

    # 定义模型
    # 使用我们的ResNet18模型，设置为2个分类
    net = ResNet18(num_classes=2)
    
    # 可选：从预训练模型加载权重(如果有)
    try:
        # 尝试加载预训练权重
        pretrained_weights = torchvision.models.ResNet18_Weights.DEFAULT
        pretrained_model = torchvision.models.resnet18(weights=pretrained_weights)
        # 复制预训练权重（除了最后的全连接层）
        pretrained_dict = {k: v for k, v in pretrained_model.state_dict().items() 
                          if k in net.state_dict() and 'fc' not in k}
        net.load_state_dict(pretrained_dict, strict=False)
        print("加载预训练ResNet18权重成功")
    except Exception as e:
        print(f"加载预训练模型失败，将使用随机初始化权重: {str(e)}")
        # 权重初始化已经在模型定义中完成


    net.to(device)

    # 定义损失函数
    loss_fn = nn.CrossEntropyLoss()

    # 定义优化器 - 使用Adam优化器，与MobileNet不同
    learning_rate = 1e-3  # 使用不同的学习率
    optimizer = torch.optim.Adam(params=net.parameters(), lr=learning_rate)
    
    # 添加学习率调度器
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.1, patience=10, verbose=True
    )

    # 禁用TensorBoard (如果有问题时)，使用普通图表可视化
    use_tensorboard = True
    writer = None
    
    if use_tensorboard:
        try:
            # 尝试创建TensorBoard写入器
            writer = SummaryWriter(log_root)
            print(f"成功创建TensorBoard日志目录: {log_root}")
        except Exception as e:
            print(f"警告: 创建TensorBoard日志时出错: {str(e)}")
            print("将继续训练但不使用TensorBoard")
            use_tensorboard = False

    # 开始训练
    epoch = 100
    total_train_step = len(train_loader)
    total_val_step = len(val_loader)
    best_accuracy = 0.0
    save_path = os.path.join(log_root, "best.pth")

    train_losses = []
    val_losses = []
    accuracies = []
    epoch_times = []  # 记录每个epoch的训练时间
    all_preds = []    # 用于混淆矩阵
    all_targets = []  # 用于混淆矩阵
    learning_rates = []  # 记录学习率变化
    
    # 记录每个类别的准确率
    class_names = list(cls_dict.values())
    class_correct = [0] * len(class_names)
    class_total = [0] * len(class_names)

    # 可视化一些训练样本
    dataiter = iter(train_loader)
    images, labels = next(dataiter)
    
    # 反归一化函数，用于可视化图像
    def imshow(inp, title=None):
        """显示tensor图像"""
        inp = inp.numpy().transpose((1, 2, 0))
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        inp = std * inp + mean
        inp = np.clip(inp, 0, 1)
        return inp
    
    # 可视化训练样本
    plt.figure(figsize=(12, 6))
    for i in range(min(8, images.size(0))):
        ax = plt.subplot(2, 4, i + 1)
        img = imshow(images[i])
        plt.imshow(img)
        plt.title(class_names[labels[i]])
        plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(log_root, "train_samples.png"))
    plt.close()

    for i in range(epoch):
        start_time = time.time()
        net.train()
        total_train_loss = 0.0
        train_bar = tqdm(train_loader, file=sys.stdout)
        for data in train_bar:
            image, target = data
            output = net(image.to(device))    # 正向传播
            loss = loss_fn(output, target.to(device))   # 计算损失
            total_train_loss += loss.item()
            # 开始优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        net.eval()
        total_val_loss = 0.0
        accurcay_sum = 0.0
        all_preds = []
        all_targets = []
        with torch.no_grad():  # 确定不调参
            val_bar = tqdm(val_loader, file=sys.stdout)
            for data in val_bar:
                image, target = data
                output = net(image.to(device))    # 正向传播
                loss = loss_fn(output, target.to(device))  # 计算损失
                total_val_loss += loss.item()
                predict_y = torch.max(output, dim=1)[1]
                accurcay_sum += torch.eq(predict_y, target.to(device)).sum().item()
                
                # 收集混淆矩阵数据
                all_preds.extend(predict_y.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
                
                # 计算每个类别的准确率
                for c in range(len(class_names)):
                    class_mask = (target == c)
                    class_correct[c] += torch.eq(predict_y[class_mask], target.to(device)[class_mask]).sum().item()
                    class_total[c] += class_mask.sum().item()

        # 计算平均损失以及精度
        train_loss = total_train_loss / total_train_step
        val_loss = total_val_loss / total_val_step
        accurcay = accurcay_sum / val_num
        epoch_time = time.time() - start_time
        epoch_times.append(epoch_time)
        
        # 更新学习率调度器
        scheduler.step(accurcay)
        current_lr = optimizer.param_groups[0]['lr']
        learning_rates.append(current_lr)
        
        print('[epoch %d] train_loss: %.3f  val_loss: %.3f  val_accuracy: %.3f  time: %.2fs  lr: %.6f' %
              (i + 1, train_loss, val_loss, accurcay, epoch_time, current_lr))
        if accurcay > best_accuracy:
            torch.save(net.state_dict(), save_path)
            best_accuracy = accurcay

        # 使用TensorBoard记录指标
        if use_tensorboard and writer is not None:
            writer.add_scalar("train_loss", train_loss, i)
            writer.add_scalar("val_loss", val_loss, i)
            writer.add_scalar("val_accuracy", accurcay, i)
            writer.add_scalar("learning_rate", current_lr, i)

        # Saving for plotting
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        accuracies.append(accurcay)
        
        # 每10个epoch保存一次图表，避免训练中断丢失结果
        if (i+1) % 10 == 0 or i == 0:
            # 保存当前进度的图表
            plt.figure(figsize=(10, 5))
            plt.plot(range(1, i + 2), train_losses, label='Training Loss')
            plt.plot(range(1, i + 2), val_losses, label='Validation Loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.title('Training and Validation Loss')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(log_root, f"loss_curve_epoch_{i+1}.png"))
            plt.close()

    # 画图
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, epoch + 1), train_losses, label='Training Loss')
    plt.plot(range(1, epoch + 1), val_losses, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(log_root, "loss_curve.png"))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, epoch + 1), accuracies, label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Validation Accuracy')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(log_root, "accuracy_curve.png"))
    plt.close()
    
    # 添加新图表：混淆矩阵
    cm = confusion_matrix(all_targets, all_preds)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    
    # 在混淆矩阵中添加数字标签
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(log_root, "confusion_matrix.png"))
    plt.close()
    
    # 添加新图表：每个类别的准确率
    plt.figure(figsize=(10, 5))
    class_accuracies = [100 * class_correct[i] / max(1, class_total[i]) for i in range(len(class_names))]
    plt.bar(range(len(class_names)), class_accuracies)
    plt.xlabel('Class')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy by Class')
    plt.xticks(range(len(class_names)), class_names, rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(log_root, "class_accuracy.png"))
    plt.close()
    
    # 添加新图表：训练时间
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, epoch + 1), epoch_times)
    plt.xlabel('Epochs')
    plt.ylabel('Time (s)')
    plt.title('Training Time per Epoch')
    plt.grid(True)
    plt.savefig(os.path.join(log_root, "epoch_time.png"))
    plt.close()
    
    # 绘制损失与准确率组合图
    plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(111)
    ln1 = ax1.plot(range(1, epoch + 1), train_losses, 'r-', label='Train Loss')
    ln2 = ax1.plot(range(1, epoch + 1), val_losses, 'b-', label='Val Loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    
    ax2 = ax1.twinx()
    ln3 = ax2.plot(range(1, epoch + 1), accuracies, 'g-', label='Accuracy')
    ax2.set_ylabel('Accuracy')
    
    lns = ln1 + ln2 + ln3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='center right')
    plt.title('Training Progress')
    plt.savefig(os.path.join(log_root, "combined_metrics.png"))
    plt.close()
    
    # 添加学习率变化图
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, epoch + 1), learning_rates)
    plt.xlabel('Epochs')
    plt.ylabel('Learning Rate')
    plt.title('Learning Rate Schedule')
    plt.yscale('log')  # 使用对数比例更好地显示变化
    plt.grid(True)
    plt.savefig(os.path.join(log_root, "learning_rate.png"))
    plt.close()
    
    # 保存最终模型评估指标
    with open(os.path.join(log_root, "final_metrics.txt"), "w") as f:
        f.write(f"模型: ResNet18\n")
        f.write(f"最佳验证准确率: {best_accuracy:.4f}\n")
        f.write("各类别准确率:\n")
        for i, name in enumerate(class_names):
            f.write(f"{name}: {class_accuracies[i]:.2f}%\n")
        f.write(f"总训练时间: {sum(epoch_times):.2f}秒\n")
        f.write(f"日志目录: {log_root}\n")

    if use_tensorboard and writer is not None:
        writer.close()
    print(f"训练完成，所有结果已保存到 {log_root}")


if __name__ == '__main__':
    main() 